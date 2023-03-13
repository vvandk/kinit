export const wxShareMixins = {
  data() {
    return {
      share: {
        title: '',
        path: '',
        imageUrl: ''
      }
    }
  },
  onLoad: function () {
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    })
  },
  onShareAppMessage(res) {
    let that = this
    let imageUrl = that.share.imageUrl || ''
    if (res.from === 'button') {
      //这块需要传参，不然链接地址进去获取不到数据
      let path = '/' + that.$scope.route + '?item=' + that.$scope.options.item
      return {
        title: '商品分享~',
        path: path,
        imageUrl: imageUrl
      }
    }
    if (res.from === 'menu') {
      return {
        title: that.share.title,
        path: that.share.path,
        imageUrl: that.share.imageUrl
      }
    }
  },
  // 分享到朋友圈
  onShareTimeline() {
    return {
      title: this.share.title,
      path: this.share.path,
      imageUrl: this.share.imageUrl
    }
  },
  methods: {}
}
