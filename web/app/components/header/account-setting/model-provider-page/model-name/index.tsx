import type { FC } from 'react'
import {
  modelTypeFormat,
  sizeFormat,
} from '../utils'
import { useLanguage } from '../hooks'
import type { ModelItem } from '../declarations'
import ModelBadge from '../model-badge'
import FeatureIcon from '../model-selector/feature-icon'

type ModelNameProps = {
  modelItem: ModelItem
  className?: string
  showModelType?: boolean
  showMode?: boolean
  showFeatures?: boolean
  showContextSize?: boolean
}
const ModelName: FC<ModelNameProps> = ({
  modelItem,
  className,
  showModelType,
  showMode,
  showFeatures,
  showContextSize,
}) => {
  const language = useLanguage()

  return (
    <div
      className={`
        flex items-center text-[13px] font-medium text-gray-800
        ${className}
      `}
    >
      <div
        className='mr-2  truncate'
        title={modelItem.label[language]}
      >
        {modelItem.label[language]}
      </div>
      {
        showModelType && (
          <ModelBadge className='mr-0.5'>
            {modelTypeFormat(modelItem.model_type)}
          </ModelBadge>
        )
      }
      {
        modelItem.model_properties.mode && showMode && (
          <ModelBadge className='mr-0.5'>
            {(modelItem.model_properties.mode as string).toLocaleUpperCase()}
          </ModelBadge>
        )
      }
      {
        showFeatures && modelItem.features?.map(feature => (
          <FeatureIcon
            key={feature}
            feature={feature}
          />
        ))
      }
      {
        showContextSize && modelItem.model_properties.context_size && (
          <ModelBadge>
            {sizeFormat(modelItem.model_properties.context_size as number)}
          </ModelBadge>
        )
      }
    </div>
  )
}

export default ModelName