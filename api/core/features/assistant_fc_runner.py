import json
import logging

from typing import Union, Generator, Dict, Any, Tuple, List

from core.model_runtime.entities.message_entities import PromptMessageTool, PromptMessage, UserPromptMessage,\
      SystemPromptMessage, AssistantPromptMessage, ToolPromptMessage
from core.model_runtime.entities.llm_entities import LLMResultChunk, LLMResult, LLMUsage
from core.model_manager import ModelInstance
from core.application_queue_manager import PublishFrom

from core.tools.provider.tool import Tool
from core.tools.errors import ToolInvokeError, ToolNotFoundError, \
    ToolNotSupportedError, ToolProviderNotFoundError, ToolParamterValidationError, \
          ToolProviderCredentialValidationError

from core.features.assistant_base_runner import BaseAssistantApplicationRunner

from extensions.ext_database import db
from models.model import Conversation, Message, MessageAgentThought

logger = logging.getLogger(__name__)

class AssistantFunctionCallApplicationRunner(BaseAssistantApplicationRunner):
    def run(self, model_instance: ModelInstance,
        conversation: Conversation,
        tool_instances: Dict[str, Tool],
        message: Message,
        prompt_messages_tools: list[PromptMessageTool],
        query: str,
    ) -> Generator[LLMResultChunk, None, None]:
        """
        Run FunctionCall agent application
        """
        app_orchestration_config = self.app_orchestration_config

        prompt_template = self.app_orchestration_config.prompt_template.simple_prompt_template or ''
        prompt_messages = self.history_prompt_messages
        prompt_messages = self.organize_prompt_messages(
            prompt_template=prompt_template,
            query=query,
            prompt_messages=prompt_messages
        )

        iteration_step = 1
        max_iteration_steps = 5

        # continue to run until there is not any tool call
        function_call_state = True
        agent_thoughts: List[MessageAgentThought] = []
        llm_usage = {
            'usage': None
        }
        final_answer = ''

        def increse_usage(final_llm_usage_dict: Dict[str, LLMUsage], usage: LLMUsage):
            if not final_llm_usage_dict['usage']:
                final_llm_usage_dict['usage'] = usage
            else:
                llm_usage = final_llm_usage_dict['usage']
                llm_usage.prompt_tokens += usage.prompt_tokens
                llm_usage.completion_tokens += usage.completion_tokens
                llm_usage.prompt_price += usage.prompt_price
                llm_usage.completion_price += usage.completion_price

        while function_call_state and iteration_step <= max_iteration_steps:
            function_call_state = False

            # recale llm max tokens
            self.recale_llm_max_tokens(self.model_config, prompt_messages)
            # invoke model
            chunks: Generator[LLMResultChunk, None, None] = model_instance.invoke_llm(
                prompt_messages=prompt_messages,
                model_parameters=app_orchestration_config.model_config.parameters,
                tools=prompt_messages_tools,
                stop=app_orchestration_config.model_config.stop,
                stream=True,
                user=self.user_id,
                callbacks=[self.agent_llm_callback],
            )

            tool_calls: List[Tuple[str, str, Dict[str, Any]]] = []

            # save full response
            response = ''

            for chunk in chunks:
                # check if there is any tool call
                if self.check_tool_calls(chunk):
                    function_call_state = True
                    tool_calls.extend(self.extract_tool_calls(chunk))

                if chunk.delta.message and chunk.delta.message.content:
                    if isinstance(chunk.delta.message.content, list):
                        for content in chunk.delta.message.content:
                            response += content.data
                    else:
                        response += chunk.delta.message.content

                if chunk.delta.usage:
                    increse_usage(llm_usage, chunk.delta.usage)

                yield chunk

            if len(agent_thoughts) > 0:
                for thought in agent_thoughts:
                    # save last agent thought's response
                    self.save_agent_thought(
                        agent_thought=thought, 
                        thought=None, 
                        observation=None, 
                        answer=response
                    )
                # clear agent thoughts of last iteration
                agent_thoughts = []

            final_answer += response + '\n'

            # call tools
            tool_responses = []
            for tool_call_id, tool_call_name, tool_call_args in tool_calls:
                tool_instance = tool_instances.get(tool_call_name)
                # create agent thought
                agent_thought = self.create_agent_thought(
                    message_id=message.id,
                    message=message.message,
                    tool_name=tool_call_name,
                    tool_input=json.dumps(tool_call_args),
                )
                agent_thoughts.append(agent_thought)
                self.queue_manager.publish_agent_thought(agent_thought, PublishFrom.APPLICATION_MANAGER)

                if not tool_instance:
                    logger.error(f"failed to find tool instance: {tool_call_name}")
                    tool_response = {
                        "tool_call_id": tool_call_id,
                        "tool_call_name": tool_call_name,
                        "tool_response": f"there is not a tool named {tool_call_name}"
                    }
                    tool_responses.append(tool_response)
                    self.save_agent_thought(
                        agent_thought=agent_thought, 
                        thought=None, 
                        observation=tool_response['tool_response'], 
                        answer=None
                    )
                    self.queue_manager.publish_agent_thought(agent_thought, PublishFrom.APPLICATION_MANAGER)
                else:
                    # invoke tool
                    error_response = None
                    try:
                        tool_invoke_message = tool_instance.invoke(
                            user_id=self.user_id, 
                            tool_paramters=tool_call_args, 
                        )
                        # transform tool invoke message to get LLM friendly message
                        tool_invoke_message = self.transform_tool_invoke_messages(tool_invoke_message)
                        # extract binary data from tool invoke message
                        binary_files = self.extract_tool_response_binary(tool_invoke_message)
                        # create message file
                        message_files = self.create_message_files(binary_files)
                        # publish files
                        for message_file, save_as_variable in message_files:
                            # save message into variables pool
                            if save_as_variable:
                                self.variables_pool.set_file(tool_name=tool_call_name, value=message_file.id)

                            # publish message file
                            self.queue_manager.publish_message_file(message_file, PublishFrom.APPLICATION_MANAGER)
                            
                    except ToolProviderCredentialValidationError as e:
                        error_response = f"Plese check your tool provider credentials"
                    except (
                        ToolNotFoundError, ToolNotSupportedError, ToolProviderNotFoundError
                    ) as e:
                        error_response = f"there is not a tool named {tool_call_name}"
                    except (
                        ToolParamterValidationError
                    ) as e:
                        error_response = f"tool paramters validation error: {e}, please check your tool paramters"
                    except ToolInvokeError as e:
                        error_response = f"tool invoke error: {e}"
                    except Exception as e:
                        error_response = f"unknown error: {e}"

                    if error_response:
                        observation = error_response
                        logger.error(error_response)
                        tool_response = {
                            "tool_call_id": tool_call_id,
                            "tool_call_name": tool_call_name,
                            "tool_response": error_response
                        }
                        tool_responses.append(tool_response)
                    else:
                        observation = self._convert_tool_response_to_str(tool_invoke_message)
                        tool_response = {
                            "tool_call_id": tool_call_id,
                            "tool_call_name": tool_call_name,
                            "tool_response": observation
                        }
                        tool_responses.append(tool_response)
                    
                    self.save_agent_thought(
                        agent_thought=agent_thought, 
                        thought=None, 
                        observation=observation, 
                        answer=None
                    )
                    self.queue_manager.publish_agent_thought(agent_thought, PublishFrom.APPLICATION_MANAGER)

                prompt_messages = self.organize_prompt_messages(
                    prompt_template=prompt_template,
                    query=None,
                    tool_call_id=tool_call_id,
                    tool_call_name=tool_call_name,
                    tool_response=tool_response['tool_response'],
                    prompt_messages=prompt_messages,
                )

            iteration_step += 1

        self.update_db_variables(self.variables_pool, self.db_variables_pool)
        # publish end event
        self.queue_manager.publish_message_end(LLMResult(
            model=model_instance.model,
            prompt_messages=prompt_messages,
            message=AssistantPromptMessage(
                content=final_answer,
            ),
            usage=llm_usage['usage'],
            system_fingerprint=''
        ), PublishFrom.APPLICATION_MANAGER)

    def check_tool_calls(self, llm_result_chunk: LLMResultChunk) -> bool:
        """
        Check if there is any tool call in llm result chunk
        """
        if llm_result_chunk.delta.message.tool_calls:
            return True
        return False

    def extract_tool_calls(self, llm_result_chunk: LLMResultChunk) -> Union[None, List[Tuple[str, str, Dict[str, Any]]]]:
        """
        Extract tool calls from llm result chunk

        Returns:
            List[Tuple[str, str, Dict[str, Any]]]: [(tool_call_id, tool_call_name, tool_call_args)]
        """
        tool_calls = []
        for prompt_message in llm_result_chunk.delta.message.tool_calls:
            tool_calls.append((
                prompt_message.id,
                prompt_message.function.name,
                json.loads(prompt_message.function.arguments),
            ))

        return tool_calls

    def organize_prompt_messages(self, prompt_template: str,
                                 query: str = None, 
                                 tool_call_id: str = None, tool_call_name: str = None, tool_response: str = None,
                                 prompt_messages: list[PromptMessage] = None
                                 ) -> list[PromptMessage]:
        """
        Organize prompt messages
        """
        
        if not prompt_messages:
            prompt_messages = [
                SystemPromptMessage(content=prompt_template),
                UserPromptMessage(content=query),
            ]
        else:
            if tool_response:
                prompt_messages = prompt_messages.copy()
                prompt_messages.append(
                    ToolPromptMessage(
                        content=tool_response,
                        tool_call_id=tool_call_id,
                        name=tool_call_name,
                    )
                )

        return prompt_messages