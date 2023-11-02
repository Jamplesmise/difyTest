import openai
import json
from typing import Optional

from core.helper.encrypter import decrypt_token
from core.moderation.base import Moderation, ModerationException
from extensions.ext_database import db
from models.provider import Provider


class OpenAIModeration(Moderation):
    name: str = "openai_moderation"

    @classmethod
    def validate_config(cls, tenant_id: str, config: dict) -> None:
        """
        Validate the incoming form config data.

        :param tenant_id: the id of workspace
        :param config: the form config data
        :return:
        """
        cls._validate_inputs_and_outputs_config(config, True)

    def moderation_for_inputs(self, inputs: dict, query: Optional[str] = None):
        if not self.config['inputs_configs']['enabled']:
            return

        preset_response = self.config['inputs_configs']['preset_response']
        if query:
            inputs['query__'] = query

        self._is_violated(inputs, preset_response)

    def moderation_for_outputs(self, text: str):
        if not self.config['outputs_configs']['enabled']:
            return

        preset_response = self.config['inputs_configs']['preset_response']

        self._is_violated({ 'text': text }, preset_response)

    def _is_violated(self, inputs: dict, preset_response: str):

        openai_api_key = self._get_openai_api_key()
        moderation_result = openai.Moderation.create(input=list(inputs.values()), api_key=openai_api_key)

        for result in moderation_result.results:
            if result['flagged']:
                raise ModerationException(preset_response)
            
    def _get_openai_api_key(self) -> str:
        provider = db.session.query(Provider) \
                    .filter_by(tenant_id=self.tenant_id) \
                    .filter_by(provider_name="openai") \
                    .first()

        if not provider:
            raise ValueError("openai provider is not configured")

        encrypted_config = json.loads(provider.encrypted_config)

        return decrypt_token(self.tenant_id, encrypted_config['openai_api_key'])