export type UserLoginType = {
  telephone: string
  password: string
}

export type UserType = {
  telephone: string
  password: string
  role: string
  roleId: string
  permissions: string | string[]
}
