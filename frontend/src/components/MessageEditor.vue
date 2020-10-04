<template>
  <b-modal ref="modal" title="Contact Form" @hidden="clear">
    <template v-slot:modal-footer="context">
      <div class="d-flex align-items-center justify-content-between flex-wrap" style="width:100%">
        <b-button variant="primary" @click="sendMessages()" :disabled="buttonsDisabled">
          <b-spinner small v-if="buttonsDisabled"></b-spinner>
          <slot name="sendButton">
            {{ $gettext('Send') }}
          </slot>
        </b-button>
        <b-button variant="danger" @click="context.ok()" :disabled="buttonsDisabled" >
          <slot name="cancelButton">
            {{ $gettext('Cancel') }}
          </slot>
        </b-button>
      </div>
    </template>
    <b-alert :show="error.length > 0"><div class="keep-newlines" >{{ error }}</div></b-alert>
    <b-form-group label="Subject">
      <b-form-input v-model="subject" :placeholder="$gettext('Subject')"></b-form-input>
    </b-form-group>
    <b-form-group label="Message">
      <b-form-textarea v-model="message" :placeholder="$gettext('Message')"></b-form-textarea>
    </b-form-group>
  </b-modal>
</template>

<script>
export default {
  name: 'SendMessageModal',
  props: ['selectedUUIDs','initialMessage','initialSubject','error'],
  data() {
    return {
      subject: this.initialMessage || '',
      message: this.initialSubject || '',
      buttonsDisabled: false,
    }
  },
  methods: {
    show() {
      this.clear()
      this.$refs.modal.show()
    },
    hide() {
      this.$refs.modal.hide()
    },
    clear() {
      this.buttonsDisabled = false
      this.subject = this.initialSubject
      this.message = this.initialMessage
    },
    sent() {
      this.buttonsDisabled = false
    },
    sendMessages() {
      this.buttonsDisabled = true
      const { subject, message } = this
      this.$emit('send', {
        subject,
        message,
        callback: () => this.sent()
      })
    }
  },
}
</script>
