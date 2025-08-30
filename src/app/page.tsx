"use client"

import { useState, useEffect } from 'react'
import { LegalDisclaimer } from '../components/legal/LegalDisclaimer'
import { DashboardStats } from '../components/dashboard/DashboardStats'
import { QuickActions } from '../components/dashboard/QuickActions'
import { RecentActivity } from '../components/dashboard/RecentActivity'
import { AIAssistant } from '../components/ai/AIAssistant'
import { AccessibilityControls } from '../components/accessibility/AccessibilityControls'
import { WelcomeHero } from '../components/dashboard/WelcomeHero'
import { NeurodivergentSupport } from '../components/accessibility/NeurodivergentSupport'

export default function HomePage() {
  const [showLegalDisclaimer, setShowLegalDisclaimer] = useState(false)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user has accepted legal disclaimer
    const hasAcceptedLegal = localStorage.getItem('neurodemon_legal_accepted')
    if (!hasAcceptedLegal) {
      setShowLegalDisclaimer(true)
    }
    
    // Simulate user loading
    setTimeout(() => {
      setLoading(false)
    }, 1000)
  }, [])

  const handleLegalAcceptance = () => {
    localStorage.setItem('neurodemon_legal_accepted', 'true')
    localStorage.setItem('neurodemon_legal_version', '1.0')
    localStorage.setItem('neurodemon_legal_accepted_at', new Date().toISOString())
    setShowLegalDisclaimer(false)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-slate-700 dark:text-slate-300 mb-2">
            Initializing NeuroDemon
          </h2>
          <p className="text-slate-600 dark:text-slate-400">
            Setting up your neurodivergent-friendly environment...
          </p>
        </div>
      </div>
    )
  }

  return (
    <>
      {showLegalDisclaimer && (
        <LegalDisclaimer 
          onAccept={handleLegalAcceptance}
          onReject={() => window.location.href = 'about:blank'}
        />
      )}

      <div className="space-y-8">
        {/* Accessibility Controls - Always visible */}
        <AccessibilityControls />

        {/* Welcome Hero Section */}
        <WelcomeHero />

        {/* Neurodivergent Support Panel */}
        <NeurodivergentSupport />

        {/* Dashboard Stats */}
        <div className="animate-fade-in">
          <DashboardStats />
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Quick Actions */}
          <div className="lg:col-span-2 animate-slide-in-from-left">
            <QuickActions />
          </div>

          {/* AI Assistant */}
          <div className="animate-slide-in-from-right">
            <AIAssistant />
          </div>
        </div>

        {/* Recent Activity */}
        <div className="animate-fade-in">
          <RecentActivity />
        </div>

        {/* Getting Started Guide for New Users */}
        {!user && (
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl p-8 border border-blue-200 dark:border-blue-800 animate-fade-in">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 dark:bg-blue-800 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-slate-800 dark:text-slate-200 mb-2">
                Welcome to NeuroDemon! 🧠
              </h3>
              <p className="text-slate-600 dark:text-slate-400 mb-6 max-w-2xl mx-auto">
                The first AI-powered penetration testing platform designed specifically for neurodivergent cybersecurity professionals. 
                Let's get you started with a personalized setup that accommodates your unique needs and preferences.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors">
                  Start Accessibility Setup
                </button>
                <button className="border border-blue-300 dark:border-blue-700 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 px-6 py-3 rounded-lg font-medium transition-colors">
                  Take Quick Tour
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Neurodivergent-Friendly Features Highlight */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-fade-in">
          <div className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-sm border border-slate-200 dark:border-slate-700">
            <div className="w-12 h-12 bg-green-100 dark:bg-green-800 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h4 className="font-semibold text-slate-800 dark:text-slate-200 mb-2">ADHD Support</h4>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Focus mode, task breakdowns, timer reminders, and progress tracking
            </p>
          </div>

          <div className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-sm border border-slate-200 dark:border-slate-700">
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-800 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h4 className="font-semibold text-slate-800 dark:text-slate-200 mb-2">Autism Friendly</h4>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Predictable workflows, detailed explanations, and routine templates
            </p>
          </div>

          <div className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-sm border border-slate-200 dark:border-slate-700">
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-800 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <h4 className="font-semibold text-slate-800 dark:text-slate-200 mb-2">Anxiety Support</h4>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Stress monitoring, gentle notifications, and confidence indicators
            </p>
          </div>

          <div className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-sm border border-slate-200 dark:border-slate-700">
            <div className="w-12 h-12 bg-orange-100 dark:bg-orange-800 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h4 className="font-semibold text-slate-800 dark:text-slate-200 mb-2">AI Guidance</h4>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Intelligent assistance, automated analysis, and natural language queries
            </p>
          </div>
        </div>
      </div>
    </>
  )
}