<template>
  <Context ref="context">
    <TableForm
      ref="form"
      :table="table"
      :default-values="table"
      @submitted="submit"
    >
      <div
        class="context__form-actions context__form-actions--multiple-actions"
      >
        <a @click="cancel">
          {{ $t('action.cancel') }}
        </a>
        <button
          type="submit"
          class="button"
          :class="{ 'button--loading': loading }"
          :disabled="loading"
        >
          {{ $t('action.save') }}
        </button>
      </div>
    </TableForm>
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'
import TableForm from '@baserow/modules/database/components/sidebar/table/TableForm'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'UpdateTableContext',
  components: { TableForm },
  mixins: [context],
  props: {
    database: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
    }
  },
  watch: {
    table() {
      // If the table values are updated via an outside source, think of real time
      // collaboration or via the modal, we want to reset the form so that it contains
      // the correct base values.
      this.reset()
    },
  },
  methods: {
    reset() {
      this.$nextTick(() => {
        this.$refs.form && this.$refs.form.reset()
      })
    },
    async submit(values) {
      this.loading = true

      try {
        await this.$store.dispatch('table/update', {
          database: this.database,
          table: this.table,
          values,
        })
        this.$refs.form && this.$refs.form.reset()
        this.loading = false
        this.hide()
        this.$emit('updated')
      } catch (error) {
        this.loading = false
        let handledByForm = false
        if (this.$refs.form) {
          handledByForm = this.$refs.form.handleErrorByForm(error)
        }
        if (!handledByForm) {
          notifyIf(error, 'table')
        }
      }
    },
    cancel() {
      this.reset()
      this.hide()
    },
  },
}
</script>
