import { useSnackbar } from 'vuetify'

export function useMessage() {
  const snackbar = useSnackbar()

  const showSuccess = (message) => {
    snackbar.add({
      color: 'success',
      text: message,
      timeout: 3000
    })
  }

  const showError = (message) => {
    snackbar.add({
      color: 'error',
      text: message,
      timeout: 5000
    })
  }

  const showWarning = (message) => {
    snackbar.add({
      color: 'warning',
      text: message,
      timeout: 4000
    })
  }

  const showInfo = (message) => {
    snackbar.add({
      color: 'info',
      text: message,
      timeout: 3000
    })
  }

  return {
    showSuccess,
    showError,
    showWarning,
    showInfo
  }
} 