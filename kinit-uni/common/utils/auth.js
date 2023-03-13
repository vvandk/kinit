const TokenKey = 'App-Token'

export function getToken() {
  return uni.getStorageSync(TokenKey)
}

export function setToken(token) {
  return uni.setStorageSync(TokenKey, token)
}

export function removeToken() {
  return uni.removeStorageSync(TokenKey)
}

const RefreshTokenKey = 'Refresh-Token'

export function getRefreshToken() {
  return uni.getStorageSync(RefreshTokenKey)
}

export function setRefreshToken(token) {
  return uni.setStorageSync(RefreshTokenKey, token)
}

export function removeRefreshToken() {
  return uni.removeStorageSync(RefreshTokenKey)
}
