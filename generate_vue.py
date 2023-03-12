import json
from datetime import datetime
from typing import List

from pypinyin import lazy_pinyin


class GenerateVue:
    @staticmethod
    def generate_vue_file(content: List[str]):
        now = datetime.now()
        file_name = "generate/MainPage " + now.strftime("%Y-%m-%d %H:%M:%S") + ".vue"
        with open(file_name, mode="w+") as f:
            f.writelines(content)

    @staticmethod
    def generate_vue_content() -> List[str]:
        content = ["""<script setup>
import { NLayout, NLayoutSider, NSpace, NInputNumber, NDivider, NSwitch, NTimeline, NTimelineItem, NButton, NDatePicker } from 'naive-ui';
import { ref } from 'vue';

let free_diamond = ref()
let paid_diamond = ref()
let star_piece = ref()
let ten_pull_ticket = ref()
let single_pull_ticket = ref()
let month_card_remain_days = ref()

let small_paid_diamond_set_count = ref()
let ten_pull_ticket_count = ref()
let large_paid_diamond_set_count = ref()

let is_month_card_purchased = ref(false)

let is_daily_draw_card = ref(false)

let extra_free_diamond = ref()
let extra_paid_diamond = ref()

let total_free_diamond = ref(0)
let total_paid_diamond = ref(0)

let timestamp = ref(167241600e4)

function computeDiamonds() {
  if (free_diamond.value === undefined) {
    free_diamond.value = 0
  }
  if (single_pull_ticket.value === undefined) {
    single_pull_ticket.value = 0
  }
  if (ten_pull_ticket.value === undefined) {
    ten_pull_ticket.value = 0
  }
  if (ten_pull_ticket_count.value === undefined) {
    ten_pull_ticket_count.value = 0
  }
  if (extra_free_diamond.value === undefined) {
    extra_free_diamond.value = 0
  }
  total_free_diamond.value = free_diamond.value
    + 150 * single_pull_ticket.value
    + 1500 * (ten_pull_ticket.value + ten_pull_ticket_count.value)
    + computeFreeDiamonds()
    + extra_free_diamond.value
  if (paid_diamond.value === undefined) {
    paid_diamond.value = 0
  }
  if (extra_paid_diamond.value === undefined) {
    extra_paid_diamond.value = 0
  }
  total_paid_diamond.value = paid_diamond.value
    + computePaidDiamonds()
    + extra_paid_diamond.value
  console.log(total_free_diamond.value)
  console.log(total_paid_diamond.value)

  if (total_free_diamond.value >= computeConsumeDiamonds()) {
    total_free_diamond.value -= computeConsumeDiamonds()
  }
  else {
    let remain_consume_diamonds = computeConsumeDiamonds() - total_free_diamond.value
    total_free_diamond.value = 0
    total_paid_diamond.value -= remain_consume_diamonds
  }
}

function computeFreeDiamonds() {
  let today = new Date()
  let end_day = new Date(timestamp.value)
  let s1 = today.getTime(), s2 = end_day.getTime()
  let total = (s2 - s1) / 1000
  let remain_days = parseInt(total / (24 * 60 * 60))

  let ret = 0
  if (is_month_card_purchased.value) {
    ret += 50 * remain_days
  }
  // 还有每日任务的钻呢
  ret += 50 * remain_days
  // 还有工资塔的钻呢
  let remain_months = Math.floor(remain_days / 30)
  ret += 1500 * remain_months
  return ret
}

function computePaidDiamonds() {
  let today = new Date()
  let end_day = new Date(timestamp.value)
  let s1 = today.getTime(), s2 = end_day.getTime()
  let total = (s2 - s1) / 1000
  let remain_days = parseInt(total / (24 * 60 * 60))
  let remain_months = Math.floor(remain_days / 30)

  let ret = 0
  if (is_month_card_purchased.value) {
    ret += 500 * remain_months
  }
  if (small_paid_diamond_set_count.value !== undefined) {
    ret += 500 * small_paid_diamond_set_count.value * remain_months
  }
  if (large_paid_diamond_set_count.value !== undefined) {
    ret += 7500 * large_paid_diamond_set_count.value * remain_months
  }
  if (is_daily_draw_card.value) {
    ret -= 75 * remain_days
  }
  return ret
}
// 这里之后是代码生成的
"""]
        with open("config/gacha_timeline_info_v2.json", encoding="utf-8") as f:
            gacha_info = json.load(f)
        for key in gacha_info.keys():
            key_pinyin = lazy_pinyin(key)
            common_key = ""
            for p in key_pinyin:
                common_key = common_key + p + "_"
            draws_key = common_key + "draws"
            stars_key = common_key + "stars"
            content.append("let {} = ref(0)\n".format(draws_key))
            content.append("let {} = ref(0)\n".format(stars_key))
            content.append("\n")
            gacha_info[key].update({"draws_key": draws_key, "stars_key": stars_key})

        content.append("function computeConsumeDiamonds() {\n")
        content.append("  let ret = 0\n")
        for key in gacha_info.keys():
            content.append("  ret += {}.value\n".format(gacha_info[key]["draws_key"]))
        content.append("  return 150 * ret\n")
        content.append("}\n")

        content.append("function computeConsumeStars() {\n")
        content.append("  let ret = 0\n")
        for key in gacha_info.keys():
            content.append("  ret += {}.value\n".format(gacha_info[key]["stars_key"]))
        content.append("  return ret\n")
        content.append("}\n\n")

        content.append("</script>")

        content.append("""<template>
  <n-layout position="absolute">
    <n-layout has-sider position="absolute" style="top: 20px; bottom: 20px;">
      <n-layout-sider bordered content-style="padding: 24px;" width="30%">
        <n-space vertical>
          <n-input-number v-model:value="free_diamond" :min="0">
            <template #prefix>免费钻</template>
          </n-input-number>
          <n-input-number v-model:value="paid_diamond" :min="0">
            <template #prefix>付费钻</template>
          </n-input-number>
          <n-input-number v-model:value="star_piece" :min="0">
            <template #prefix>星碎</template>
          </n-input-number>
          <n-input-number v-model:value="ten_pull_ticket" :min="0">
            <template #prefix>十连券</template>
          </n-input-number>
          <n-input-number v-model:value="single_pull_ticket" :min="0">
            <template #prefix>单抽券</template>
          </n-input-number>
          <n-input-number v-model:value="month_card_remain_days" :min="0">
            <template #prefix>月卡还有几天到期？</template>
          </n-input-number>
          <n-divider />
          <n-switch v-model:value="is_month_card_purchased">
            <template #checked>我买月卡</template>
            <template #unchecked>我不买月卡</template>
          </n-switch>
          <n-input-number v-model:value="small_paid_diamond_set_count" :min="0">
            <template #prefix>每个月 25 买几次？</template>
          </n-input-number>
          <n-input-number v-model:value="ten_pull_ticket_count" :min="0">
            <template #prefix>每个月 98 买几次？</template>
          </n-input-number>
          <n-input-number v-model:value="large_paid_diamond_set_count" :min="0">
            <template #prefix>每个月 518 买几次？</template>
          </n-input-number>
          <n-divider />
          <n-switch v-model:value="is_daily_draw_card">
            <template #checked>抽TM的！</template>
            <template #unchecked>我就不每日单抽</template>
          </n-switch>
          <n-input-number v-model:value="extra_free_diamond" :min="0">
            <template #prefix>额外免费钻</template>
          </n-input-number>
          <n-input-number v-model:value="extra_paid_diamond" :min="0">
            <template #prefix>额外付费钻</template>
          </n-input-number>
          <n-divider />
          <n-button @click="computeDiamonds">
            点击计算
          </n-button>
            等价免费钻剩余：{{ total_free_diamond }}
        </n-space>
      </n-layout-sider>
      <n-layout content-style="padding: 24px;" :native-scrollbar="false">
        <n-timeline>
""")
        for key in gacha_info.keys():
            content.append("          <n-timeline-item type=\"{}\" title=\"{}\" time=\"{}\">\n".format(gacha_info[key]["type"], key, gacha_info[key]["start_time"]))
            content.append("            <n-space vertical #default>\n")
            content.append("              {}\n".format(gacha_info[key]["description"]))
            content.append("              <n-input-number v-model:value=\"{}\" :min=\"0\">\n".format(gacha_info[key]["draws_key"]))
            content.append("                <template #prefix>投入多少抽？</template>\n")
            content.append("              </n-input-number>\n")
            content.append("              <n-input-number v-model:value=\"{}\" :min=\"0\">\n".format(gacha_info[key]["stars_key"]))
            content.append("                <template #prefix>投入多少星碎？</template>\n")
            content.append("              </n-input-number>\n")
            content.append("            </n-space>\n")
            content.append("          </n-timeline-item>\n")
        content.append("        </n-timeline>\n")
        content.append("      </n-layout>\n")
        content.append("    </n-layout>\n")
        content.append("  </n-layout>\n")
        content.append("</template>\n\n")

        content.append("""<style>
</style>
""")
        return content


if __name__ == '__main__':
    GenerateVue.generate_vue_file(GenerateVue.generate_vue_content())
    # print(GenerateVue.generate_vue_content())
