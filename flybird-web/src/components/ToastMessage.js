import { createVNode, render } from 'vue'
import ToastMessageVue from './ToastMessage.vue'

const div = document.createElement('div')
div.setAttribute('class', 'toast-message')
document.body.appendChild(div)

export const showToast = (message, type = 'info') => {
    const vnode = createVNode(ToastMessageVue, {
        message,
        type,
        duration: 2000,
        onDestroy: () => {
            render(null, div)
        }
    })
    
    render(vnode, div)
}

export default showToast