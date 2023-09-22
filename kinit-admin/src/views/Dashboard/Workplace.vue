<script setup lang="ts">
import { useTimeAgo } from '@/hooks/web/useTimeAgo'
import { ElRow, ElCol, ElSkeleton, ElCard, ElDivider, ElLink } from 'element-plus'
import { useI18n } from '@/hooks/web/useI18n'
import { ref, reactive, computed } from 'vue'
import { formatTime, getGreeting, getCurrentDate, getDayOfWeek } from '@/utils'
import { Highlight } from '@/components/Highlight'
import {
  getProjectApi,
  getDynamicApi,
  getTeamApi,
  getShortcutsApi
} from '@/api/dashboard/workplace'
import type { Project, Dynamic, Team, Shortcuts } from '@/api/dashboard/workplace/types'
import avatar from '@/assets/imgs/avatar.jpg'
import { useAuthStore } from '@/store/modules/auth'

defineOptions({
  name: 'DashboardWorkplace'
})

const authStore = useAuthStore()

const loading = ref(true)

const toLink = (link: string) => {
  window.open(link)
}

let projects = reactive<Project[]>([])

// 获取项目数
const getProject = async () => {
  const res = await getProjectApi().catch(() => {})
  if (res) {
    projects = Object.assign(projects, res.data)
  }
}

let shortcuts = reactive<Shortcuts[]>([])

// 获取快捷操作
const getShortcuts = async () => {
  const res = await getShortcutsApi().catch(() => {})
  if (res) {
    shortcuts = Object.assign(shortcuts, res.data)
  }
}

getShortcuts()

// 获取动态
let dynamics = reactive<Dynamic[]>([])

const getDynamic = async () => {
  const res = await getDynamicApi().catch(() => {})
  if (res) {
    dynamics = Object.assign(dynamics, res.data)
  }
}

// 获取团队
let team = reactive<Team[]>([])

const getTeam = async () => {
  const res = await getTeamApi().catch(() => {})
  if (res) {
    team = Object.assign(team, res.data)
  }
}

const getAllApi = async () => {
  await Promise.all([getProject(), getDynamic(), getTeam()])
  loading.value = false
}

getAllApi()

const { t } = useI18n()

const user = computed(() => authStore.getUser)
</script>

<template>
  <div class="bg-[var(--app-content-bg-color)] flex-grow">
    <div>
      <ElCard shadow="never">
        <ElSkeleton :loading="loading" animated>
          <ElRow :gutter="20" justify="space-between">
            <ElCol :xl="12" :lg="12" :md="12" :sm="24" :xs="24">
              <div class="flex items-center">
                <img
                  :src="user.avatar ? user.avatar : avatar"
                  alt=""
                  class="w-70px h-70px rounded-[50%] mr-20px"
                />
                <div>
                  <div class="text-20px">
                    {{ getGreeting() }}，{{ user.name }}，{{ t('workplace.happyDay') }}
                  </div>
                  <div class="mt-10px text-14px text-gray-500">
                    {{ getCurrentDate() }}，{{ getDayOfWeek() }}
                  </div>
                </div>
              </div>
            </ElCol>
            <ElCol :xl="12" :lg="12" :md="12" :sm="24" :xs="24">
              <div class="flex h-70px items-center justify-end <sm:mt-20px">
                <div class="px-8px text-right">
                  <div class="text-14px text-gray-400 mb-20px">最近登录时间</div>
                  <span class="text-20px">{{ user.last_login?.split(' ')[0] }}</span>
                </div>
              </div>
            </ElCol>
          </ElRow>
        </ElSkeleton>
      </ElCard>
    </div>

    <div class="mx-20px mt-20px">
      <ElRow :gutter="20" justify="space-between">
        <ElCol :xl="16" :lg="16" :md="24" :sm="24" :xs="24" class="mb-20px">
          <ElCard shadow="never">
            <template #header>
              <div class="flex justify-between">
                <span>{{ t('workplace.project') }}</span>
                <ElLink type="primary" :underline="false">{{ t('workplace.more') }}</ElLink>
              </div>
            </template>
            <ElSkeleton :loading="loading" animated>
              <ElRow>
                <ElCol
                  v-for="(item, index) in projects"
                  :key="`card-${index}`"
                  :xl="8"
                  :lg="8"
                  :md="12"
                  :sm="24"
                  :xs="24"
                >
                  <ElCard shadow="hover">
                    <div class="cursor-pointer" @click="toLink(item.link)">
                      <div class="flex items-center">
                        <Icon :icon="item.icon" :size="25" class="mr-10px" />
                        <span class="text-16px">{{ item.name }}</span>
                      </div>
                      <div class="mt-15px text-14px text-gray-400">{{ t(item.message) }}</div>
                      <div class="mt-20px text-12px text-gray-400 flex justify-between">
                        <span>{{ item.personal }}</span>
                        <span>{{ formatTime(item.time, 'yyyy-MM-dd') }}</span>
                      </div>
                    </div>
                  </ElCard>
                </ElCol>
              </ElRow>
            </ElSkeleton>
          </ElCard>

          <ElCard shadow="never" class="mt-20px">
            <template #header>
              <div class="flex justify-between">
                <span>{{ t('workplace.dynamic') }}</span>
                <ElLink type="primary" :underline="false">{{ t('workplace.more') }}</ElLink>
              </div>
            </template>
            <ElSkeleton :loading="loading" animated>
              <div v-for="(item, index) in dynamics" :key="`dynamics-${index}`">
                <div class="flex items-center">
                  <img
                    src="@/assets/imgs/avatar.jpg"
                    alt=""
                    class="w-35px h-35px rounded-[50%] mr-20px"
                  />
                  <div>
                    <div class="text-14px">
                      <Highlight :keys="item.keys.map((v) => t(v))">
                        {{ t('workplace.pushCode') }}
                      </Highlight>
                    </div>
                    <div class="mt-15px text-12px text-gray-400">
                      {{ useTimeAgo(item.time) }}
                    </div>
                  </div>
                </div>
                <ElDivider />
              </div>
            </ElSkeleton>
          </ElCard>
        </ElCol>
        <ElCol :xl="8" :lg="8" :md="24" :sm="24" :xs="24" class="mb-20px">
          <ElCard shadow="never">
            <template #header>
              <span>{{ t('workplace.shortcutOperation') }}</span>
            </template>
            <ElSkeleton :loading="loading" animated>
              <ElCol
                v-for="(item, index) in shortcuts"
                :key="`card-${index}`"
                :xl="12"
                :lg="12"
                :md="12"
                :sm="12"
                :xs="12"
                class="mb-10px"
              >
                <ElLink type="primary" :href="item.link" target="_blank" :underline="false">
                  {{ item.name }}
                </ElLink>
              </ElCol>
            </ElSkeleton>
          </ElCard>

          <ElCard shadow="never" class="mt-20px">
            <template #header>
              <span>{{ t('workplace.team') }}</span>
            </template>
            <ElSkeleton :loading="loading" animated>
              <ElRow>
                <ElCol v-for="item in team" :key="`team-${item.name}`" :span="12" class="mb-20px">
                  <div class="flex items-center">
                    <Icon :icon="item.icon" class="mr-10px" />
                    <ElLink type="default" :underline="false">
                      {{ item.name }}
                    </ElLink>
                  </div>
                </ElCol>
              </ElRow>
            </ElSkeleton>
          </ElCard>
        </ElCol>
      </ElRow>
    </div>
  </div>
</template>
