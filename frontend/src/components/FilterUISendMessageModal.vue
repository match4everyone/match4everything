<template>
  <b-modal ref="modal" title="Contact Form" @hidden="clear">
    <template v-slot:modal-footer="context">
      <div class="d-flex align-items-center justify-content-between flex-wrap" style="width:100%">
        <b-button variant="primary" @click="sendMessages()" >
          Contact all selected
        </b-button>
        <b-button variant="danger" @click="context.ok()" >
          Close
        </b-button>
      </div>
    </template>
    <b-form-group label="Subject">
      <b-form-input v-model="subject" placeholder="Subject"></b-form-input>
    </b-form-group>
    <b-form-group label="message">
      <b-form-textarea v-model="message" placeholder="Message"></b-form-textarea>
    </b-form-group>
  </b-modal>
</template>

<script>
import Cookies from 'js-cookie'


export default {
  name: 'FilterUISendMessageModal',
  props: ['selectedUUIDs'],
  data() {
    return {
      subject: '',
      message: '',
      url: window.location.href,
      csrftoken: Cookies.get('csrftoken'),
    }
  },
  methods: {
    show() {
      this.$refs.modal.show()
    },
    hide() {
      this.$refs.modal.hide()
    },
    clear() {
      this.subject = this.message = ''
    },
    sendMessages() {
      if (!Array.isArray(this.selectedUUIDs) || this.selectedUUIDs.length === 0) {
        return
      }
      let formData = new FormData()
      this.selectedUUIDs.forEach(uuid => formData.append('uuid',uuid))
      formData.append('uuid', 'e2f1e4b6-000d-45e2-83d5-85b8783f5ec4')
      formData.append('msg-only-subject', this.subject)
      formData.append('msg-only-contact_text',this.message)

      fetch('https://coding-machine/matching/helper/?location_country_code=DE&location_zipcode=22952&location_distance=50', {
        method: 'POST',
        headers: {'X-CSRFToken': this.csrftoken},
        body: formData,
      })
        .then(response => response.json())
        .then(json => {
          if (json.success) {
            this.$emit('sent',json.message)
          } else {
            this.$emit('error',json.message)
          }
          console.log('Message sending response',json.success,json.message,json)
        })
        .catch(error => {
          this.$emit('error','Messages could not be send, please try again later')
          console.error('Unexpexted error sending messages:', error)
        })
      this.hide()
    }
  },
}
</script>
