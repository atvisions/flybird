<template>
    <transition name="toast">
        <div v-if="visible" :class="['toast-container', type]">
            {{ message }}
        </div>
    </transition>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue'

const props = defineProps({
    message: {
        type: String,
        required: true
    },
    type: {
        type: String,
        default: 'info'
    },
    duration: {
        type: Number,
        default: 2000
    },
    onDestroy: {
        type: Function,
        required: true
    }
})

const visible = ref(false)

onMounted(() => {
    visible.value = true
    setTimeout(() => {
        visible.value = false
        setTimeout(() => {
            props.onDestroy()
        }, 200) // 等待过渡动画结束
    }, props.duration)
})
</script>

<style scoped>
.toast-container {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px 20px;
    border-radius: 4px;
    color: white;
    font-size: 14px;
    z-index: 9999;
}

.success {
    background-color: #67c23a;
}

.warning {
    background-color: #e6a23c;
}

.error {
    background-color: #f56c6c;
}

.info {
    background-color: #909399;
}

.toast-enter-active,
.toast-leave-active {
    transition: opacity 0.2s, transform 0.2s;
}

.toast-enter-from,
.toast-leave-to {
    opacity: 0;
    transform: translate(-50%, -20px);
}
</style>

