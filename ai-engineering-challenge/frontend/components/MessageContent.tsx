'use client'

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'

type MessageContentProps = {
  content: string
  isTyping?: boolean
  displayedText?: string
}

export default function MessageContent({ content, isTyping, displayedText }: MessageContentProps) {
  const [copiedCode, setCopiedCode] = useState<string | null>(null)

  const copyToClipboard = async (code: string, id: string) => {
    try {
      await navigator.clipboard.writeText(code)
      setCopiedCode(id)
      setTimeout(() => setCopiedCode(null), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const textToRender = isTyping ? displayedText || '' : content

  return (
    <div className="markdown-content">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={{
          code({ node, inline, className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || '')
            const codeString = String(children).replace(/\n$/, '')
            const codeId = `code-${Math.random().toString(36).substr(2, 9)}`

            if (!inline && match) {
              return (
                <div className="code-block-wrapper">
                  <button
                    onClick={() => copyToClipboard(codeString, codeId)}
                    className="copy-button"
                  >
                    {copiedCode === codeId ? '✓ Copied!' : 'Copy'}
                  </button>
                  <pre>
                    <code className={className} {...props}>
                      {children}
                    </code>
                  </pre>
                </div>
              )
            }

            return (
              <code className={className} {...props}>
                {children}
              </code>
            )
          },
        }}
      >
        {textToRender}
      </ReactMarkdown>
    </div>
  )
}
