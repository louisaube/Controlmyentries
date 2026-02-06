import { useState, useEffect, useCallback, useRef } from 'react'
import { ProgressData } from '@/types'

interface UseWebSocketOptions {
  jobId: string | null
  onComplete?: (downloadUrl: string) => void
  onError?: (error: string) => void
}

interface UseWebSocketReturn {
  progress: ProgressData | null
  isConnected: boolean
  connect: () => void
  disconnect: () => void
}

export function useWebSocket({
  jobId,
  onComplete,
  onError,
}: UseWebSocketOptions): UseWebSocketReturn {
  const [progress, setProgress] = useState<ProgressData | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)

  const connect = useCallback(() => {
    if (!jobId || wsRef.current) return

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}/ws/progress/${jobId}`

    try {
      const ws = new WebSocket(wsUrl)
      wsRef.current = ws

      ws.onopen = () => {
        setIsConnected(true)
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          setProgress({
            step: data.step,
            stepName: data.step_name,
            progress: data.progress,
            anomaliesFound: data.anomalies_found || 0,
            status: data.status,
          })

          if (data.status === 'complete' && data.download_url) {
            onComplete?.(data.download_url)
          }

          if (data.status === 'error') {
            onError?.(data.message || 'Erreur inconnue')
          }
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e)
        }
      }

      ws.onerror = () => {
        onError?.('Connexion WebSocket perdue')
        setIsConnected(false)
      }

      ws.onclose = () => {
        setIsConnected(false)
        wsRef.current = null
      }
    } catch (e) {
      onError?.('Impossible de se connecter au WebSocket')
    }
  }, [jobId, onComplete, onError])

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    setIsConnected(false)
    setProgress(null)
  }, [])

  // Auto-connect when jobId changes
  useEffect(() => {
    if (jobId) {
      connect()
    }
    return () => {
      disconnect()
    }
  }, [jobId, connect, disconnect])

  return {
    progress,
    isConnected,
    connect,
    disconnect,
  }
}
