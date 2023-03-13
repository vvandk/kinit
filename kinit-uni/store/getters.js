const getters = {
  isUser: (state) => state.auth.isUser,
  isUserOpenid: (state) => state.auth.isUserOpenid,
  isResetPassword: (state) => state.auth.isResetPassword,
  token: (state) => state.auth.token,
  avatar: (state) => state.auth.avatar,
  name: (state) => state.auth.name,
  roles: (state) => state.auth.roles,
  permissions: (state) => state.auth.permissions,
  telephone: (state) => state.auth.telephone,

  version: (state) => state.app.version,
  title: (state) => state.app.title,
  logo: (state) => state.app.logo,
  logoImage: (state) => state.app.logoImage,
  footer: (state) => state.app.footer,
  footerContent: (state) => state.app.footerContent,
  icpNumber: (state) => state.app.icpNumber,
  privacy: (state) => state.app.privacy,
  agreement: (state) => state.app.agreement,
  siteUrl: (state) => state.app.siteUrl,
  WXEmail: (state) => state.app.WXEmail,
  WXPhone: (state) => state.app.WXPhone,
  dictObj: (state) => state.dict.dictObj
}
export default getters
