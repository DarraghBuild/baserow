// This mixin is used to check if a user is a super admin
export default {
  data() {
    return {
      superAdmins: {},
    }
  },
  created() {
    this.superAdmins = this.$env.SUPER_ADMINS.split(',').map((s) => s.trim()).reduce((acc, item) => {
      acc[item] = true
      return acc
    }, {})
  },
  methods: {
    isSuperAdmin(user) {
      return user.email && this.superAdmins[user.email]
    }
  }
}