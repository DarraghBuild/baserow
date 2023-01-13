<template>
  <form class="context__form" @submit.prevent="submit">
    <FormElement :error="fieldHasErrors('name')" class="control">
      <div class="control__elements">
        <input
          ref="name"
          v-model="values.name"
          :class="{ 'input--error': fieldHasErrors('name') }"
          type="text"
          class="input"
          placeholder="Table"
          @blur="$v.values.name.$touch()"
        />
        <div
          v-if="$v.values.name.$dirty && !$v.values.name.required"
          class="error"
        >
          {{ $t('error.requiredField') }}
        </div>
        <div
          v-else-if="$v.values.name.$dirty && !$v.values.name.maxLength"
          class="error"
        >
          {{ $t('error.nameTooLong') }}
        </div>
      </div>
    </FormElement>
    <FormElement :error="fieldHasErrors('api_name')" class="control">
      <div class="control__elements">
        <input
          ref="api_name"
          v-model="values.api_name"
          :class="{ 'input--error': fieldHasErrors('api_name') }"
          type="text"
          class="input"
          placeholder="api_name"
          @focus="apiNameFocus()"
          @blur="$v.values.api_name.$touch(); apiNameUnfocus()"
        />
        <div
          v-if="$v.values.api_name.$dirty && !$v.values.api_name.required"
          class="error"
        >
          {{ $t('error.requiredField') }}
        </div>
        <div
          v-else-if="
            $v.values.api_name.$dirty && !$v.values.api_name.mustUseValidAPINameCharacters
          "
          class="error"
        >
          Not a valid API name format.
        </div>
        <div
          v-else-if="$v.values.api_name.$dirty && !$v.values.api_name.maxLength"
          class="error"
        >
          {{ $t('error.nameTooLong') }}
        </div>
        <div
          v-else-if="api_name_focused"
          class="warning"
        >
          Warning: Changing the API name<br>
          might break API integrations!
        </div>
      </div>
    </FormElement>
    <slot></slot>
  </form>
</template>

<script>
import { required, maxLength } from 'vuelidate/lib/validators'

import form from '@baserow/modules/core/mixins/form'
import {
  MAX_FIELD_NAME_LENGTH,
} from '@baserow/modules/database/utils/constants'

// @TODO focus form on open
export default {
  name: 'TableForm',
  mixins: [form],
  props: {
    table: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      allowedValues: ['name', 'api_name'],
      values: {
        name: '',
        api_name: '',
      },
      api_name_focused: false,
    }
  },
  computed: {
    existingTableId() {
      return this.defaultValues ? this.defaultValues.id : null
    },
  },
  validations() {
    return {
      values: {
        name: {
          required,
          maxLength: maxLength(MAX_FIELD_NAME_LENGTH),
        },
        api_name: {
          required,
          maxLength: maxLength(MAX_FIELD_NAME_LENGTH),
          mustUseValidAPINameCharacters: this.mustUseValidAPINameCharacters,
        },
      },
    }
  },
  methods: {
    mustUseValidAPINameCharacters(param) {
      param = param.trim()
      return /^[a-z0-9_]+$/.test(param) && param.slice(0) !== "_" && param.slice(-1) !== "_" && !(/__/.test(param))
    },
    apiNameFocus() {
      if (this.apiNameWarningInterval) {
        clearInterval(this.apiNameWarningInterval);
      }

      this.api_name_focused = true;
    },
    apiNameUnfocus() {
      this.apiNameWarningInterval = setInterval(() => {
        this.api_name_focused = false;
      }, 500);
    },
  },
}
</script>
