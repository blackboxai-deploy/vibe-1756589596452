"use client"

import React, { createContext, useContext, useState, useEffect } from 'react'

interface AccessibilitySettings {
  theme: 'light' | 'dark' | 'high-contrast' | 'calm'
  fontSize: 'small' | 'medium' | 'large' | 'extra-large'
  animations: 'full' | 'reduced' | 'none'
  sounds: 'enabled' | 'minimal' | 'disabled'
  focusMode: boolean
  timerReminders: boolean
  stressMonitoring: boolean
  neurodivergentSupport: {
    adhd: boolean
    autism: boolean
    anxiety: boolean
    ocd: boolean
    ptsd: boolean
  }
}

interface AccessibilityContextType {
  settings: AccessibilitySettings
  updateSettings: (settings: Partial<AccessibilitySettings>) => void
  resetSettings: () => void
}

const defaultSettings: AccessibilitySettings = {
  theme: 'calm',
  fontSize: 'medium',
  animations: 'reduced',
  sounds: 'minimal',
  focusMode: false,
  timerReminders: true,
  stressMonitoring: true,
  neurodivergentSupport: {
    adhd: true,
    autism: true,
    anxiety: true,
    ocd: false,
    ptsd: false
  }
}

const AccessibilityContext = createContext<AccessibilityContextType | undefined>(undefined)

export function AccessibilityProvider({ children }: { children: React.ReactNode }) {
  const [settings, setSettings] = useState<AccessibilitySettings>(defaultSettings)

  useEffect(() => {
    // Load settings from localStorage on mount
    const savedSettings = localStorage.getItem('neurodemon_accessibility')
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings)
        setSettings({ ...defaultSettings, ...parsed })
      } catch (error) {
        console.error('Failed to parse accessibility settings:', error)
      }
    }
  }, [])

  useEffect(() => {
    // Save settings to localStorage whenever they change
    localStorage.setItem('neurodemon_accessibility', JSON.stringify(settings))
    
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', settings.theme)
    document.documentElement.setAttribute('data-font-size', settings.fontSize)
    document.documentElement.setAttribute('data-animations', settings.animations)
    
    // Apply accessibility classes
    if (settings.focusMode) {
      document.body.classList.add('focus-mode')
    } else {
      document.body.classList.remove('focus-mode')
    }
  }, [settings])

  const updateSettings = (newSettings: Partial<AccessibilitySettings>) => {
    setSettings(prev => ({ ...prev, ...newSettings }))
  }

  const resetSettings = () => {
    setSettings(defaultSettings)
  }

  return (
    <AccessibilityContext.Provider value={{ settings, updateSettings, resetSettings }}>
      {children}
    </AccessibilityContext.Provider>
  )
}

export function useAccessibility() {
  const context = useContext(AccessibilityContext)
  if (context === undefined) {
    throw new Error('useAccessibility must be used within an AccessibilityProvider')
  }
  return context
}