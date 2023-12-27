from core.model_runtime.entities.llm_entities import LLMMode
from core.model_runtime.entities.model_entities import ModelFeature, ModelType, FetchFrom, ParameterRule, \
    DefaultParameterName, PriceConfig
from core.model_runtime.entities.model_entities import AIModelEntity, I18nObject
from core.model_runtime.entities.defaults import PARAMETER_RULE_TEMPLATE

AZURE_OPENAI_API_VERSION = '2023-12-01-preview'


def _get_max_tokens(default: int, min_val: int, max_val: int) -> ParameterRule:
    rule = ParameterRule(
        name='max_tokens',
        **PARAMETER_RULE_TEMPLATE[DefaultParameterName.MAX_TOKENS],
    )
    rule.default = default
    rule.min = min_val
    rule.max = max_val
    return rule


LLM_BASE_MODELS = [
    {
        'base_model_name': 'gpt-35-turbo',
        'entity': AIModelEntity(
            model='gpt-3.5-turbo',
            label=I18nObject(
                en_US='gpt-3.5-turbo',
            ),
            model_type=ModelType.LLM,
            features=[
                ModelFeature.AGENT_THOUGHT,
                ModelFeature.MULTI_TOOL_CALL,
            ],
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties={
                'mode': LLMMode.CHAT,
                'context_size': 4096,
            },
            parameter_rules=[
                ParameterRule(
                    name='temperature',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TEMPERATURE],
                ),
                ParameterRule(
                    name='top_p',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TOP_P],
                ),
                ParameterRule(
                    name='presence_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.PRESENCE_PENALTY],
                ),
                ParameterRule(
                    name='frequency_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.FREQUENCY_PENALTY],
                ),
                _get_max_tokens(default=512, min_val=1, max_val=4096)
            ],
            price=PriceConfig(
                input=0.001,
                output=0.002,
                unit=0.001,
                currency='USD',
            )
        )
    },
    {
        'base_model_name': 'gpt-35-turbo-16k',
        'entity': AIModelEntity(
            model='gpt-3.5-turbo-16k',
            label=I18nObject(
                en_US='gpt-3.5-turbo-16k',
            ),
            model_type=ModelType.LLM,
            features=[
                ModelFeature.AGENT_THOUGHT,
                ModelFeature.MULTI_TOOL_CALL,
            ],
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties={
                'mode': LLMMode.CHAT,
                'context_size': 16385,
            },
            parameter_rules=[
                ParameterRule(
                    name='temperature',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TEMPERATURE],
                ),
                ParameterRule(
                    name='top_p',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TOP_P],
                ),
                ParameterRule(
                    name='presence_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.PRESENCE_PENALTY],
                ),
                ParameterRule(
                    name='frequency_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.FREQUENCY_PENALTY],
                ),
                _get_max_tokens(default=512, min_val=1, max_val=16385)
            ],
            price=PriceConfig(
                input=0.003,
                output=0.004,
                unit=0.001,
                currency='USD',
            )
        )
    },
    {
        'base_model_name': 'gpt-4',
        'entity': AIModelEntity(
            model='gpt-4',
            label=I18nObject(
                en_US='gpt-4',
            ),
            model_type=ModelType.LLM,
            features=[
                ModelFeature.AGENT_THOUGHT,
                ModelFeature.MULTI_TOOL_CALL,
            ],
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties={
                'mode': LLMMode.CHAT,
                'context_size': 8192,
            },
            parameter_rules=[
                ParameterRule(
                    name='temperature',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TEMPERATURE],
                ),
                ParameterRule(
                    name='top_p',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TOP_P],
                ),
                ParameterRule(
                    name='presence_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.PRESENCE_PENALTY],
                ),
                ParameterRule(
                    name='frequency_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.FREQUENCY_PENALTY],
                ),
                _get_max_tokens(default=512, min_val=1, max_val=8192),
                ParameterRule(
                    name='seed',
                    label=I18nObject(
                        zh_Hans='种子',
                        en_US='Seed'
                    ),
                    type='int',
                    help=I18nObject(
                        zh_Hans='如果指定，模型将尽最大努力进行确定性采样，使得重复的具有相同种子和参数的请求应该返回相同的结果。不能保证确定性，您应该参考 system_fingerprint 响应参数来监视变化。',
                        en_US='If specified, model will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed, and you should refer to the system_fingerprint response parameter to monitor changes in the backend.'
                    ),
                    required=False,
                    precision=2,
                    min=0,
                    max=1,
                ),
                ParameterRule(
                    name='response_format',
                    label=I18nObject(
                        zh_Hans='回复格式',
                        en_US='response_format'
                    ),
                    type='string',
                    help=I18nObject(
                        zh_Hans='指定模型必须输出的格式',
                        en_US='specifying the format that the model must output'
                    ),
                    required=False,
                    options=['text', 'json_object']
                ),
            ],
            price=PriceConfig(
                input=0.03,
                output=0.06,
                unit=0.001,
                currency='USD',
            )
        )
    },
    {
        'base_model_name': 'gpt-4-32k',
        'entity': AIModelEntity(
            model='gpt-4-32k',
            label=I18nObject(
                en_US='gpt-4-32k',
            ),
            model_type=ModelType.LLM,
            features=[
                ModelFeature.AGENT_THOUGHT,
                ModelFeature.MULTI_TOOL_CALL,
            ],
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties={
                'mode': LLMMode.CHAT,
                'context_size': 32768,
            },
            parameter_rules=[
                ParameterRule(
                    name='temperature',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TEMPERATURE],
                ),
                ParameterRule(
                    name='top_p',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TOP_P],
                ),
                ParameterRule(
                    name='presence_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.PRESENCE_PENALTY],
                ),
                ParameterRule(
                    name='frequency_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.FREQUENCY_PENALTY],
                ),
                _get_max_tokens(default=512, min_val=1, max_val=32768),
                ParameterRule(
                    name='seed',
                    label=I18nObject(
                        zh_Hans='种子',
                        en_US='Seed'
                    ),
                    type='int',
                    help=I18nObject(
                        zh_Hans='如果指定，模型将尽最大努力进行确定性采样，使得重复的具有相同种子和参数的请求应该返回相同的结果。不能保证确定性，您应该参考 system_fingerprint 响应参数来监视变化。',
                        en_US='If specified, model will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed, and you should refer to the system_fingerprint response parameter to monitor changes in the backend.'
                    ),
                    required=False,
                    precision=2,
                    min=0,
                    max=1,
                ),
                ParameterRule(
                    name='response_format',
                    label=I18nObject(
                        zh_Hans='回复格式',
                        en_US='response_format'
                    ),
                    type='string',
                    help=I18nObject(
                        zh_Hans='指定模型必须输出的格式',
                        en_US='specifying the format that the model must output'
                    ),
                    required=False,
                    options=['text', 'json_object']
                ),
            ],
            price=PriceConfig(
                input=0.06,
                output=0.12,
                unit=0.001,
                currency='USD',
            )
        )
    },
    {
        'base_model_name': 'gpt-4-1106-preview',
        'entity': AIModelEntity(
            model='gpt-4-1106-preview',
            label=I18nObject(
                en_US='gpt-4-1106-preview',
            ),
            model_type=ModelType.LLM,
            features=[
                ModelFeature.AGENT_THOUGHT,
                ModelFeature.MULTI_TOOL_CALL,
            ],
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties={
                'mode': LLMMode.CHAT,
                'context_size': 128000,
            },
            parameter_rules=[
                ParameterRule(
                    name='temperature',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TEMPERATURE],
                ),
                ParameterRule(
                    name='top_p',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TOP_P],
                ),
                ParameterRule(
                    name='presence_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.PRESENCE_PENALTY],
                ),
                ParameterRule(
                    name='frequency_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.FREQUENCY_PENALTY],
                ),
                _get_max_tokens(default=512, min_val=1, max_val=128000),
                ParameterRule(
                    name='seed',
                    label=I18nObject(
                        zh_Hans='种子',
                        en_US='Seed'
                    ),
                    type='int',
                    help=I18nObject(
                        zh_Hans='如果指定，模型将尽最大努力进行确定性采样，使得重复的具有相同种子和参数的请求应该返回相同的结果。不能保证确定性，您应该参考 system_fingerprint 响应参数来监视变化。',
                        en_US='If specified, model will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed, and you should refer to the system_fingerprint response parameter to monitor changes in the backend.'
                    ),
                    required=False,
                    precision=2,
                    min=0,
                    max=1,
                ),
                ParameterRule(
                    name='response_format',
                    label=I18nObject(
                        zh_Hans='回复格式',
                        en_US='response_format'
                    ),
                    type='string',
                    help=I18nObject(
                        zh_Hans='指定模型必须输出的格式',
                        en_US='specifying the format that the model must output'
                    ),
                    required=False,
                    options=['text', 'json_object']
                ),
            ],
            price=PriceConfig(
                input=0.01,
                output=0.03,
                unit=0.001,
                currency='USD',
            )
        )
    },
    {
        'base_model_name': 'gpt-4-vision-preview',
        'entity': AIModelEntity(
            model='gpt-4-vision-preview',
            label=I18nObject(
                en_US='gpt-4-vision-preview',
            ),
            model_type=ModelType.LLM,
            features=[
                ModelFeature.VISION
            ],
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties={
                'mode': LLMMode.CHAT,
                'context_size': 128000,
            },
            parameter_rules=[
                ParameterRule(
                    name='temperature',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TEMPERATURE],
                ),
                ParameterRule(
                    name='top_p',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TOP_P],
                ),
                ParameterRule(
                    name='presence_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.PRESENCE_PENALTY],
                ),
                ParameterRule(
                    name='frequency_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.FREQUENCY_PENALTY],
                ),
                _get_max_tokens(default=512, min_val=1, max_val=128000),
                ParameterRule(
                    name='seed',
                    label=I18nObject(
                        zh_Hans='种子',
                        en_US='Seed'
                    ),
                    type='int',
                    help=I18nObject(
                        zh_Hans='如果指定，模型将尽最大努力进行确定性采样，使得重复的具有相同种子和参数的请求应该返回相同的结果。不能保证确定性，您应该参考 system_fingerprint 响应参数来监视变化。',
                        en_US='If specified, model will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed, and you should refer to the system_fingerprint response parameter to monitor changes in the backend.'
                    ),
                    required=False,
                    precision=2,
                    min=0,
                    max=1,
                ),
                ParameterRule(
                    name='response_format',
                    label=I18nObject(
                        zh_Hans='回复格式',
                        en_US='response_format'
                    ),
                    type='string',
                    help=I18nObject(
                        zh_Hans='指定模型必须输出的格式',
                        en_US='specifying the format that the model must output'
                    ),
                    required=False,
                    options=['text', 'json_object']
                ),
            ],
            price=PriceConfig(
                input=0.01,
                output=0.03,
                unit=0.001,
                currency='USD',
            )
        )
    },
    {
        'base_model_name': 'gpt-35-turbo-instruct',
        'entity': AIModelEntity(
            model='gpt-35-turbo-instruct',
            label=I18nObject(
                en_US='gpt-35-turbo-instruct',
            ),
            model_type=ModelType.LLM,
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties={
                'mode': LLMMode.COMPLETION,
                'context_size': 4096,
            },
            parameter_rules=[
                ParameterRule(
                    name='temperature',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TEMPERATURE],
                ),
                ParameterRule(
                    name='top_p',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.TOP_P],
                ),
                ParameterRule(
                    name='presence_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.PRESENCE_PENALTY],
                ),
                ParameterRule(
                    name='frequency_penalty',
                    **PARAMETER_RULE_TEMPLATE[DefaultParameterName.FREQUENCY_PENALTY],
                ),
                _get_max_tokens(default=512, min_val=1, max_val=4096),
            ],
            price=PriceConfig(
                input=0.0015,
                output=0.002,
                unit=0.001,
                currency='USD',
            )
        )
    }
]

EMBEDDING_BASE_MODELS = [
    {
        'base_model_name': 'text-embedding-ada-002',
        'entity': AIModelEntity(
            model='text-embedding-ada-002',
            label=I18nObject(
                en_US='text-embedding-ada-002'
            ),
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_type=ModelType.TEXT_EMBEDDING,
            model_properties={
                'context_size': 8097,
                'max_chunks': 32,
            }
        )
    }
]