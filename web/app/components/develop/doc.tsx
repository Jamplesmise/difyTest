'use client'
import { useContext } from 'use-context-selector'
import TemplateEn from './template/template.en.mdx'
import TemplateZh from './template/template.zh.mdx'
import TemplateChatEn from './template/template_chat.en.mdx'
import TemplateChatZh from './template/template_chat.zh.mdx'
import I18n from '@/context/i18n'
import { LanguagesSupportedUnderscore, getModelRuntimeSupported } from '@/utils/language'

type IDocProps = {
  appDetail: any
}

const Doc = ({ appDetail }: IDocProps) => {
  const { locale } = useContext(I18n)
  const language = getModelRuntimeSupported(locale)
  const variables = appDetail?.model_config?.configs?.prompt_variables || []
  const inputs = variables.reduce((res: any, variable: any) => {
    res[variable.key] = variable.name || ''
    return res
  }, {})

  return (
    <article className="prose prose-xl" >
      {appDetail?.mode === 'completion'
        ? (
          language !== LanguagesSupportedUnderscore[1] ? <TemplateEn appDetail={appDetail} variables={variables} inputs={inputs} /> : <TemplateZh appDetail={appDetail} variables={variables} inputs={inputs} />
        )
        : (
          language !== LanguagesSupportedUnderscore[1] ? <TemplateChatEn appDetail={appDetail} variables={variables} inputs={inputs} /> : <TemplateChatZh appDetail={appDetail} variables={variables} inputs={inputs} />
        )}
    </article>
  )
}

export default Doc
