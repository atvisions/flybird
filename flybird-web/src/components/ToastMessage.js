import { createVNode, render, getCurrentInstance } from 'vue'
import ToastMessageVue from './ToastMessage.vue'

const div = document.createElement('div')
div.setAttribute('class', 'toast-message')
document.body.appendChild(div)

export const showToast = (message, type = 'info', duration = 3000) => {
    const vnode = createVNode(ToastMessageVue, {
        message,
        type,
        duration: 2000,
        onDestroy: () => {
            render(null, div)
        }
    })
    
    render(vnode, div)

    const app = getCurrentInstance()?.appContext.app
    if (app) {
        app.config.globalProperties.toastMessage = message
        app.config.globalProperties.toastType = type
        app.config.globalProperties.toastDuration = duration
    }
}

export default showToast