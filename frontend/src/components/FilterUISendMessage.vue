<template>
  <message-editor :error="errorMessage" @send="sendMessages" ref="editor">
    <template v-slot:sendButton>
      {{ $gettext('Contact all selected') }}
    </template>
  </message-editor>
</template>

<script>
import MessageEditor from './MessageEditor'

export default {
  name: 'FilterUISendMessage',
  props: ['selectedUUIDs'],
  components: { MessageEditor },
  data() {
    return {
      errorMessage: ''
    }
  },
  methods: {
    show() {
      this.errorMessage = ''
      this.$refs.editor.show()
    },
    sendMessages(data) {
      this.errorMessage = ''
      if (!Array.isArray(this.selectedUUIDs) || this.selectedUUIDs.length === 0) {
        this.errorMessage = this.$gettext('No recipients selected, can\'t send a message')
        return
      }
      let formData = new FormData()
      this.selectedUUIDs.forEach(uuid => formData.append('uuid',uuid))
      formData.append('msg-only-subject', data.subject)
      formData.append('msg-only-contact_text',data.message)

      fetch('', {
        method: 'POST',
        headers: {'X-CSRFToken': this.$getToken()},
        body: formData,
      })
        .then(response => response.json())
        .then(json => {
          if (json.success) {
            this.$refs.editor.hide()
            this.$emit('sent',json.message)
          } else {
            this.errorMessage = json.message
          }
          console.debug('Message sending response',json.success,json.message,json)
        })
        .catch(error => {
          this.errorMessage = this.$gettext('Messages could not be send, please try again later')
          console.error('Unexpected error sending messages:', error)
        })
        .finally(() => data.callback())
    }
  },
}
</script>
