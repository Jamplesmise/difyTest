'use client'
import type { FC } from 'react'
import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import EditItem, { EditItemType } from './edit-item'
import Drawer from '@/app/components/base/drawer-plus'
import { MessageCheckRemove } from '@/app/components/base/icons/src/vender/line/communication'
import DeleteConfirmModal from '@/app/components/base/modal/delete-confirm-modal'

type Props = {
  isShow: boolean
  onHide: () => void
  query: string
  answer: string
  onSave: (editedQuery: string, editedAnswer: string) => void
  id: string
  createdAt: string
  onRemove: () => void
}

const EditReplyModal: FC<Props> = ({
  isShow,
  onHide,
  query,
  answer,
  onSave,
  id,
  createdAt,
  onRemove,
}) => {
  const { t } = useTranslation()

  const handleSave = (type: EditItemType, editedContent: string) => {
    if (type === EditItemType.Query)
      onSave(editedContent, answer)
    else
      onSave(query, editedContent)
  }
  const [showModal, setShowModal] = useState(false)

  return (
    <div>
      <Drawer
        isShow={isShow}
        onHide={onHide}
        title={t('appDebug.feature.annotation.editModal.title') as string}
        body={(
          <div className='p-6 pb-4 space-y-6'>
            <EditItem
              type={EditItemType.Query}
              content={query}
              onSave={editedContent => handleSave(EditItemType.Query, editedContent)}
            />
            <EditItem
              type={EditItemType.Answer}
              content={answer}
              onSave={editedContent => handleSave(EditItemType.Answer, editedContent)}
            />
          </div>
        )}
        foot={id
          ? (
            <div className='px-4 flex h-16 items-center justify-between border-t border-black/5 bg-gray-50 rounded-bl-xl rounded-br-xl leading-[18px] text-[13px] font-medium text-gray-500'>
              <div
                className='flex items-center pl-3 space-x-2 cursor-pointer'
                onClick={() => setShowModal(true)}
              >
                <MessageCheckRemove />
                <div>{t('appDebug.feature.annotation.editModal.removeThisCache')}</div>
              </div>
              <div>{t('appDebug.feature.annotation.editModal.createdAt')}&nbsp;{createdAt}</div>
            </div>
          )
          : undefined}
      >
      </Drawer>
      <DeleteConfirmModal
        isShow={showModal}
        onHide={() => setShowModal(false)}
        onRemove={() => {
          onRemove()
          setShowModal(false)
        }}
        text={t('appDebug.feature.annotation.removeConfirm') as string}
      />
    </div>

  )
}
export default React.memo(EditReplyModal)
