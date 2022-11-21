<template>
  <li>
    <a
      href="/api-docs"
      target="_blank"
      class="dashboard__sidebar-link"
    >
      <i class="fas fa-fw fa-book"></i>
      {{ $t('databaseDashboardSidebarLinks.apiDocumentation') }}
    </a>
  </li>
</template>

<script>
export default {
  name: 'DatabaseDashboardSidebarLinks',
}
</script>
