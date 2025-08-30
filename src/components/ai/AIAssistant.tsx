"use client"

import { useState } from 'react'

export function AIAssistant() {
  const [message, setMessage] = useState('')
  const [conversation, setConversation] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m NeuroAI, your penetration testing assistant. I\'m here to help with neurodivergent-friendly guidance, tool recommendations, and security analysis. How can I assist you today?'
    }
  ])

  const handleSendMessage = async () => {
    if (!message.trim()) return

    const newConversation = [
      ...conversation,
      { role: 'user', content: message }
    ]

    setConversation(newConversation)
    setMessage('')

    // Simulate AI response (would connect to backend)
    setTimeout(() => {
      const responses = [
        "I understand you're working on network scanning. Let me break this down into manageable steps for you...",
        "Based on your target environment, I recommend starting with a gentle ping sweep to avoid triggering security systems.",
        "For ADHD-friendly workflow, I suggest setting a 25-minute timer for this task. Would you like me to explain the process step by step?"
      ]
      
      setConversation(prev => [
        ...prev,
        { 
          role: 'assistant', 
          content: responses[Math.floor(Math.random() * responses.length)]
        }
      ])
    }, 1000)
  }

  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-sm border border-slate-200 dark:border-slate-700 h-96 flex flex-col">
      <div className="flex items-center space-x-2 mb-4">
        <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
          <span className="text-white text-sm font-bold">AI</span>
        </div>
        <div>
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">NeuroAI Assistant</h3>
          <p className="text-xs text-slate-500 dark:text-slate-400">Neurodivergent-friendly guidance</p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 mb-4">
        {conversation.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-lg text-sm ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-100 dark:bg-slate-700 text-slate-900 dark:text-slate-100'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
      </div>

      <div className="flex space-x-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Ask for guidance, tool recommendations, or analysis..."
          className="flex-1 px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleSendMessage}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm transition-colors"
        >
          Send
        </button>
      </div>
    </div>
  )
}