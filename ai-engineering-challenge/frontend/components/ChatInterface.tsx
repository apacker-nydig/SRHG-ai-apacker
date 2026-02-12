'use client'

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useTypingEffect } from '@/hooks/useTypingEffect'
import { useLocalStorage } from '@/hooks/useLocalStorage'
import MessageContent from '@/components/MessageContent'
import confetti from 'canvas-confetti'

type Message = {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
  isTyping?: boolean
  reaction?: 'up' | 'down' | null
}

function TypingMessage({ content }: { content: string }) {
  const { displayedText } = useTypingEffect(content, 20)
  return <MessageContent content={content} isTyping displayedText={displayedText} />
}

function formatTime(timestamp: number): string {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`

  const diffHours = Math.floor(diffMins / 60)
  if (diffHours < 24) return `${diffHours}h ago`

  return date.toLocaleDateString()
}

function generateTitle(messages: Message[]): string {
  const firstUserMessage = messages.find((m) => m.role === 'user')
  if (!firstUserMessage) return 'New Chat'
  const words = firstUserMessage.content.split(' ').slice(0, 5)
  return words.join(' ') + (firstUserMessage.content.split(' ').length > 5 ? '...' : '')
}

export default function ChatInterface() {
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isDark, setIsDark] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [soundEnabled, setSoundEnabled] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const {
    conversations,
    currentConversationId,
    getCurrentConversation,
    updateConversation,
    createNewConversation,
    deleteConversation,
    switchConversation,
  } = useLocalStorage()

  const currentConvo = getCurrentConversation()
  const messages: Message[] = currentConvo?.messages || []

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light')
  }, [isDark])

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + 'px'
    }
  }, [input])

  const playSound = (type: 'send' | 'receive') => {
    if (!soundEnabled) return
    const audio = new Audio(type === 'send' ? '/sounds/send.mp3' : '/sounds/receive.mp3')
    audio.volume = 0.3
    audio.play().catch(() => {}) // Ignore errors if sound files don't exist
  }

  const triggerConfetti = () => {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#667eea', '#764ba2', '#f093fb', '#4facfe'],
    })
  }

  const reactToMessage = (messageId: string, reaction: 'up' | 'down') => {
    if (!currentConvo) return

    const updatedMessages = currentConvo.messages.map((msg: Message) =>
      msg.id === messageId
        ? { ...msg, reaction: msg.reaction === reaction ? null : reaction }
        : msg
    )

    updateConversation(currentConvo.id, { messages: updatedMessages })

    // Trigger confetti on thumbs up
    if (reaction === 'up') {
      triggerConfetti()
    }
  }

  const sendMessage = async () => {
    if (!input.trim() || isLoading || !currentConvo) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: Date.now(),
    }

    const updatedMessages = [...currentConvo.messages, userMessage]
    updateConversation(currentConvo.id, {
      messages: updatedMessages,
      title: currentConvo.messages.length === 0 ? generateTitle([userMessage]) : currentConvo.title,
    })

    setInput('')
    setIsLoading(true)
    playSound('send')

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      })

      let data
      let errorText = ''

      try {
        const text = await response.text()
        errorText = text
        data = JSON.parse(text)
      } catch (e) {
        data = null
      }

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${errorText}`)
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.reply,
        timestamp: Date.now(),
        isTyping: true,
        reaction: null,
      }

      updateConversation(currentConvo.id, {
        messages: [...updatedMessages, assistantMessage],
      })

      playSound('receive')
    } catch (error) {
      console.error('Error sending message:', error)

      let errorDetails = 'Unknown error'
      if (error instanceof Error) {
        errorDetails = error.message
      } else {
        errorDetails = String(error)
      }

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `❌ Error: ${errorDetails}\n\nStack: ${error instanceof Error ? error.stack : 'N/A'}`,
        timestamp: Date.now(),
        isTyping: false,
      }

      updateConversation(currentConvo.id, {
        messages: [...updatedMessages, errorMessage],
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Cmd+K or Ctrl+K for new chat
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault()
      createNewConversation()
      return
    }

    // Send on Cmd+Enter (Mac) or Ctrl+Enter (Windows/Linux)
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      e.preventDefault()
      sendMessage()
    }
    // Send on Enter (without shift)
    else if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className={`w-full h-screen flex ${isDark ? 'gradient-bg-dark' : 'gradient-bg'}`}>
      {/* Sidebar */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ x: -300, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -300, opacity: 0 }}
            className="w-80 glass border-r border-opacity-20 flex flex-col"
            style={{ borderColor: 'var(--border-color)' }}
          >
            <div className="p-4 border-b border-opacity-20" style={{ borderColor: 'var(--border-color)' }}>
              <button
                onClick={() => createNewConversation()}
                className="w-full px-4 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-all font-medium flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                New Chat (⌘K)
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-2 custom-scrollbar">
              {conversations.map((convo) => (
                <div
                  key={convo.id}
                  className={`p-3 rounded-lg mb-2 cursor-pointer transition-all group ${
                    convo.id === currentConversationId
                      ? 'bg-blue-500 bg-opacity-20'
                      : 'hover:bg-opacity-10 hover:bg-gray-500'
                  }`}
                  onClick={() => switchConversation(convo.id)}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1 min-w-0">
                      <p
                        className="font-medium truncate"
                        style={{ color: 'var(--text-primary)' }}
                      >
                        {convo.title}
                      </p>
                      <p
                        className="text-xs mt-1"
                        style={{ color: 'var(--text-secondary)' }}
                      >
                        {formatTime(convo.updatedAt)}
                      </p>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        deleteConversation(convo.id)
                      }}
                      className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-500 hover:bg-opacity-20 rounded transition-all"
                      title="Delete conversation"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <div className="p-4 border-t border-opacity-20 space-y-2" style={{ borderColor: 'var(--border-color)' }}>
              <button
                onClick={() => setSoundEnabled(!soundEnabled)}
                className="w-full px-4 py-2 glass rounded-lg hover:bg-opacity-20 hover:bg-gray-500 transition-all flex items-center justify-between"
                style={{ color: 'var(--text-primary)' }}
              >
                <span>Sound Effects</span>
                <span>{soundEnabled ? '🔊' : '🔇'}</span>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Chat Area */}
      <div className="flex-1 flex items-center justify-center p-4">
        <div className="w-full max-w-4xl h-[85vh] flex flex-col glass rounded-2xl shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="p-6 border-b border-opacity-20" style={{ borderColor: 'var(--border-color)' }}>
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setSidebarOpen(!sidebarOpen)}
                  className="p-2 rounded-lg hover:bg-opacity-10 hover:bg-gray-500 transition-all"
                  aria-label="Toggle sidebar"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                </button>
                <div>
                  <h1 className="text-3xl font-bold" style={{ color: 'var(--text-primary)' }}>
                    Ari's Local Helper
                  </h1>
                  <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>
                    Terse robot assistant
                  </p>
                </div>
              </div>

              {/* Dark mode toggle */}
              <button
                onClick={() => setIsDark(!isDark)}
                className="p-3 rounded-full hover:bg-opacity-10 hover:bg-gray-500 transition-all duration-300"
                aria-label="Toggle dark mode"
              >
                {isDark ? (
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" />
                  </svg>
                ) : (
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                  </svg>
                )}
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
            {messages.length === 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center mt-20"
                style={{ color: 'var(--text-secondary)' }}
              >
                <p className="text-2xl font-semibold mb-2">Awaiting input.</p>
                <p className="text-base">
                  State query.
                </p>
              </motion.div>
            )}

            <AnimatePresence>
              {messages.map((message, index) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  transition={{
                    type: 'spring',
                    stiffness: 200,
                    damping: 20,
                    delay: index * 0.05
                  }}
                  className={`flex ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  } items-start gap-3`}
                >
                  {/* Avatar */}
                  {message.role === 'assistant' && (
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-white font-bold shadow-lg flex-shrink-0">
                      AL
                    </div>
                  )}

                  <div className="flex flex-col max-w-[70%]">
                    <div
                      className={`rounded-2xl p-4 shadow-lg ${
                        message.role === 'user'
                          ? 'bg-blue-500 text-white'
                          : 'glass'
                      }`}
                      style={
                        message.role === 'assistant'
                          ? { color: 'var(--ai-text)' }
                          : undefined
                      }
                    >
                      {message.role === 'assistant' && message.isTyping ? (
                        <TypingMessage content={message.content} />
                      ) : (
                        <MessageContent content={message.content} />
                      )}
                    </div>

                    {/* Timestamp and reactions */}
                    <div className="flex items-center gap-2 mt-1 px-2">
                      <span
                        className="text-xs"
                        style={{ color: 'var(--text-secondary)' }}
                        title={new Date(message.timestamp).toLocaleString()}
                      >
                        {formatTime(message.timestamp)}
                      </span>

                      {/* Reaction buttons (only for assistant messages) */}
                      {message.role === 'assistant' && (
                        <div className="flex gap-1">
                          <button
                            onClick={() => reactToMessage(message.id, 'up')}
                            className={`text-sm p-1 rounded transition-all ${
                              message.reaction === 'up'
                                ? 'bg-green-100 dark:bg-green-900'
                                : 'hover:bg-gray-100 dark:hover:bg-gray-800'
                            }`}
                            title="Helpful"
                          >
                            👍
                          </button>
                          <button
                            onClick={() => reactToMessage(message.id, 'down')}
                            className={`text-sm p-1 rounded transition-all ${
                              message.reaction === 'down'
                                ? 'bg-red-100 dark:bg-red-900'
                                : 'hover:bg-gray-100 dark:hover:bg-gray-800'
                            }`}
                            title="Not helpful"
                          >
                            👎
                          </button>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* User avatar */}
                  {message.role === 'user' && (
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-white font-bold shadow-lg flex-shrink-0">
                      YOU
                    </div>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>

            {isLoading && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex justify-start items-start gap-3"
              >
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-white font-bold shadow-lg">
                  AL
                </div>
                <div className="glass rounded-2xl p-4 shadow-lg">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce"></div>
                    <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce-delay-100"></div>
                    <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce-delay-200"></div>
                  </div>
                </div>
              </motion.div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-6 border-t border-opacity-20" style={{ borderColor: 'var(--border-color)' }}>
            <div className="flex space-x-3">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your message... (Enter to send, Shift+Enter for new line)"
                className="flex-1 p-4 glass rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all min-h-[56px] max-h-[150px]"
                style={{ color: 'var(--text-primary)' }}
                rows={1}
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={!input.trim() || isLoading}
                className="px-8 py-4 bg-blue-500 text-white rounded-xl hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95 shadow-lg font-medium"
              >
                Send
              </button>
            </div>
            <p className="text-xs mt-2 text-center" style={{ color: 'var(--text-secondary)' }}>
              Tip: Press Enter to send, ⌘K for new chat
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
