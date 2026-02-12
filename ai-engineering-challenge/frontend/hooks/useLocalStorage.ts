'use client'

import { useState, useEffect } from 'react'

export type Conversation = {
  id: string
  title: string
  messages: any[]
  createdAt: number
  updatedAt: number
}

export function useLocalStorage() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null)

  // Load conversations from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem('ego-check-conversations')
    if (stored) {
      const parsed = JSON.parse(stored)
      setConversations(parsed)
      if (parsed.length > 0) {
        setCurrentConversationId(parsed[0].id)
      }
    } else {
      // Create first conversation
      const firstConvo: Conversation = {
        id: Date.now().toString(),
        title: 'New Chat',
        messages: [],
        createdAt: Date.now(),
        updatedAt: Date.now(),
      }
      setConversations([firstConvo])
      setCurrentConversationId(firstConvo.id)
    }
  }, [])

  // Save conversations to localStorage whenever they change
  useEffect(() => {
    if (conversations.length > 0) {
      localStorage.setItem('ego-check-conversations', JSON.stringify(conversations))
    }
  }, [conversations])

  const getCurrentConversation = () => {
    return conversations.find((c) => c.id === currentConversationId) || null
  }

  const updateConversation = (id: string, updates: Partial<Conversation>) => {
    setConversations((prev) =>
      prev.map((c) =>
        c.id === id
          ? { ...c, ...updates, updatedAt: Date.now() }
          : c
      )
    )
  }

  const createNewConversation = () => {
    const newConvo: Conversation = {
      id: Date.now().toString(),
      title: 'New Chat',
      messages: [],
      createdAt: Date.now(),
      updatedAt: Date.now(),
    }
    setConversations((prev) => [newConvo, ...prev])
    setCurrentConversationId(newConvo.id)
    return newConvo.id
  }

  const deleteConversation = (id: string) => {
    setConversations((prev) => {
      const filtered = prev.filter((c) => c.id !== id)
      if (filtered.length === 0) {
        // Create a new conversation if we deleted the last one
        const newConvo: Conversation = {
          id: Date.now().toString(),
          title: 'New Chat',
          messages: [],
          createdAt: Date.now(),
          updatedAt: Date.now(),
        }
        setCurrentConversationId(newConvo.id)
        return [newConvo]
      }
      // If we deleted the current conversation, switch to the first one
      if (id === currentConversationId) {
        setCurrentConversationId(filtered[0].id)
      }
      return filtered
    })
  }

  const switchConversation = (id: string) => {
    setCurrentConversationId(id)
  }

  return {
    conversations,
    currentConversationId,
    getCurrentConversation,
    updateConversation,
    createNewConversation,
    deleteConversation,
    switchConversation,
  }
}
