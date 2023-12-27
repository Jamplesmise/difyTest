import type { FC } from 'react'
import type {
  Model,
  ModelProvider,
} from '../declarations'
import { useLanguage } from '../hooks'
import { CubeOutline } from '@/app/components/base/icons/src/vender/line/shapes'

type ModelIconProps = {
  provider?: Model | ModelProvider
  className?: string
}
const ModelIcon: FC<ModelIconProps> = ({
  provider,
  className,
}) => {
  const language = useLanguage()

  if (provider?.icon_small) {
    return (
      <img
        alt='model-icon'
        src={`${provider.icon_small[language]}?_token=${localStorage.getItem('console_token')}`}
        className={`w-4 h-4 ${className}`}
      />
    )
  }

  return (
    <div className={`
      flex items-center justify-center w-6 h-6 rounded border-[0.5px] border-black/5 bg-gray-50
      ${className}
    `}>
      <CubeOutline className='w-4 h-4 text-gray-400' />
    </div>
  )
}

export default ModelIcon