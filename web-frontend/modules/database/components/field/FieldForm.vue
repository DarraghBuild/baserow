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
          :placeholder="$t('fieldForm.name')"
          @blur="$v.values.name.$touch()"
        />
        <div
          v-if="$v.values.name.$dirty && !$v.values.name.required"
          class="error"
        >
          {{ $t('error.requiredField') }}
        </div>
        <div
          v-else-if="
            $v.values.name.$dirty && !$v.values.name.mustHaveUniqueFieldName
          "
          class="error"
        >
          {{ $t('fieldForm.fieldAlreadyExists') }}
        </div>
        <div
          v-else-if="
            $v.values.name.$dirty &&
            !$v.values.name.mustNotClashWithReservedName
          "
          class="error"
        >
          {{ $t('error.nameNotAllowed') }}
        </div>
        <div
          v-else-if="$v.values.name.$dirty && !$v.values.name.maxLength"
          class="error"
        >
          {{ $t('error.nameTooLong') }}
        </div>
      </div>
    </FormElement>
    <FormElement v-if="!creating" :error="fieldHasErrors('api_name')" class="control">
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
            $v.values.api_name.$dirty && !$v.values.api_name.mustHaveUniqueFieldAPIName
          "
          class="error"
        >
          {{ $t('fieldForm.fieldAlreadyExists') }}
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
    <div v-if="forcedType === null" class="control">
      <div class="control__elements">
        <Dropdown
          v-model="values.type"
          :class="{ 'dropdown--error': $v.values.type.$error }"
          @hide="$v.values.type.$touch()"
        >
          <DropdownItem
            v-for="(fieldType, type) in fieldTypes"
            :key="type"
            :icon="fieldType.iconClass"
            :name="fieldType.getName()"
            :value="fieldType.type"
            :disabled="primary && !fieldType.canBePrimaryField"
          ></DropdownItem>
        </Dropdown>
        <div v-if="$v.values.type.$error" class="error">
          {{ $t('error.requiredField') }}
        </div>
      </div>
    </div>
    <template v-if="hasFormComponent">
      <component
        :is="getFormComponent(values.type)"
        ref="childForm"
        :table="table"
        :field-type="values.type"
        :name="values.name"
        :default-values="defaultValues"
        @validate="$v.$touch"
      />
    </template>
    <slot></slot>
  </form>
</template>

<script>
import { required, maxLength } from 'vuelidate/lib/validators'

import form from '@baserow/modules/core/mixins/form'
import { mapGetters } from 'vuex'
import {
  RESERVED_BASEROW_FIELD_NAMES,
  MAX_FIELD_NAME_LENGTH,
} from '@baserow/modules/database/utils/constants'

// @TODO focus form on open
export default {
  name: 'FieldForm',
  mixins: [form],
  props: {
    table: {
      type: Object,
      required: true,
    },
    primary: {
      type: Boolean,
      required: false,
      default: false,
    },
    forcedType: {
      type: [String, null],
      required: false,
      default: null,
    },
    creating: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    let data = {
      allowedValues: ['name', 'type'],
      values: {
        name: '',
        type: this.forcedType || '',
      },
      api_name_focused: false,
    }

    if (!this.creating) {
      data.allowedValues.push('api_name')
      data.values.api_name = ''
    }

    return data
  },
  computed: {
    fieldTypes() {
      return this.$registry.getAll('field')
    },
    hasFormComponent() {
      return !!this.values.type && this.getFormComponent(this.values.type)
    },
    existingFieldId() {
      return this.defaultValues ? this.defaultValues.id : null
    },
    ...mapGetters({
      fields: 'field/getAll',
    }),
  },
  validations() {
    let validations = {
      values: {
        name: {
          required,
          maxLength: maxLength(MAX_FIELD_NAME_LENGTH),
          mustHaveUniqueFieldName: this.mustHaveUniqueFieldName,
          mustNotClashWithReservedName: this.mustNotClashWithReservedName,
        },
        type: { required },
      },
    }

    if (!this.creating) {
      validations.values.api_name = {
        required,
        maxLength: maxLength(MAX_FIELD_NAME_LENGTH),
        mustHaveUniqueFieldAPIName: this.mustHaveUniqueFieldAPIName,
        mustUseValidAPINameCharacters: this.mustUseValidAPINameCharacters,
      }
    }

    return validations
  },
  methods: {
    mustHaveUniqueFieldName(param) {
      let fields = this.fields
      if (this.existingFieldId !== null) {
        fields = fields.filter((f) => f.id !== this.existingFieldId)
      }
      return !fields.map((f) => f.name).includes(param.trim())
    },
    mustHaveUniqueFieldAPIName(param) {
      let fields = this.fields
      if (this.existingFieldId !== null) {
        fields = fields.filter((f) => f.id !== this.existingFieldId)
      }
      return !fields.map((f) => f.api_name).includes(param.trim())
    },
    mustUseValidAPINameCharacters(param) {
      param = param.trim()
      return /^[a-z0-9_]+$/.test(param) && param.slice(0) !== "_" && param.slice(-1) !== "_" && !(/__/.test(param))
    },
    mustNotClashWithReservedName(param) {
      return !RESERVED_BASEROW_FIELD_NAMES.includes(param.trim())
    },
    getFormComponent(type) {
      return this.$registry.get('field', type).getFormComponent()
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
