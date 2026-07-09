import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import TelaLogin from './Login'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <TelaLogin />
  </StrictMode>,
)
