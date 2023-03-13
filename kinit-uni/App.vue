<script>
export default {
  onLaunch: function () {
    this.initApp()
  },
  methods: {
    // 初始化应用
    initApp() {
      // 初始化应用配置
      this.$store.dispatch('app/InitConfig')
    }
  }
}
</script>

<style lang="scss">
@import '@/static/scss/index.scss';
</style>
