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
import { NLayout, NLayoutSider, NSpace, NInputNumber, NDivider, NSwitch, NTimeline, NTimelineItem, NButton } from 'naive-ui';
import { ref } from 'vue';

let free_diamond = ref(0)
let paid_diamond = ref(0)
let star_piece = ref(0)
let ten_pull_ticket = ref(0)
let single_pull_ticket = ref(0)
let month_card_remain_days = ref(0)

let small_paid_diamond_set_count = ref(0)
let ten_pull_ticket_count = ref(0)
let large_paid_diamond_set_count = ref(0)

let is_month_card_purchased = ref(false)

let is_daily_draw_card = ref(false)

let extra_free_diamond = ref(20000)
let extra_paid_diamond = ref(0)


let total_free_diamond = ref(0)
let total_paid_diamond = ref(0)

function computeDiamonds () {
  total_free_diamond.value = free_diamond.value 
                           + 150 * single_pull_ticket.value 
                           + 1500 * (ten_pull_ticket.value + ten_pull_ticket_count.value)
                           + computeFreeDiamonds()
                           + extra_free_diamond.value
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

function computeFreeDiamonds () {
  let today = new Date()
  let end_day = new Date("2022/12/31")
  let s1 = today.getTime(), s2 = end_day.getTime()
  let total = (s2 - s1) / 1000
  let remain_days = parseInt(total / (24 * 60 * 60))

  let ret = 0
  if (is_month_card_purchased.value) {
    ret += 50 * remain_days
  }
  return ret
}

function computePaidDiamonds() {
  let today = new Date()
  let end_day = new Date("2022/12/31")
  let s1 = today.getTime(), s2 = end_day.getTime()
  let total = (s2 - s1) / 1000
  let remain_days = parseInt(total / (24 * 60 * 60))
  let remain_months = Math.floor(remain_days / 30)

  let ret = 0
  if (is_month_card_purchased.value) {
    ret += 500 * remain_months
  }
  ret += 500 * small_paid_diamond_set_count.value * remain_months
  ret += 7500 * large_paid_diamond_set_count.value * remain_months
  if (is_daily_draw_card.value) {
    ret -= 75 * remain_days
  }
  return ret
}
// ??????????????????????????????
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
            <template #prefix>?????????</template>
          </n-input-number>
          <n-input-number v-model:value="paid_diamond" :min="0">
            <template #prefix>?????????</template>
          </n-input-number>
          <n-input-number v-model:value="star_piece" :min="0">
            <template #prefix>??????</template>
          </n-input-number>
          <n-input-number v-model:value="ten_pull_ticket" :min="0">
            <template #prefix>?????????</template>
          </n-input-number>
          <n-input-number v-model:value="single_pull_ticket" :min="0">
            <template #prefix>?????????</template>
          </n-input-number>
          <n-input-number v-model:value="month_card_remain_days" :min="0">
            <template #prefix>???????????????????????????</template>
          </n-input-number>
          <n-divider />
          <n-switch v-model:value="is_month_card_purchased">
            <template #checked>????????????</template>
            <template #unchecked>???????????????</template>
          </n-switch>
          <n-input-number v-model:value="small_paid_diamond_set_count" :min="0">
            <template #prefix>????????? 25 ????????????</template>
          </n-input-number>
          <n-input-number v-model:value="ten_pull_ticket_count" :min="0">
            <template #prefix>????????? 98 ????????????</template>
          </n-input-number>
          <n-input-number v-model:value="large_paid_diamond_set_count" :min="0">
            <template #prefix>????????? 518 ????????????</template>
          </n-input-number>
          <n-divider />
          <n-switch v-model:value="is_daily_draw_card">
            <template #checked>???TM??????</template>
            <template #unchecked>?????????????????????</template>
          </n-switch>
          <n-input-number v-model:value="extra_free_diamond" :min="0">
            <template #prefix>???????????????</template>
          </n-input-number>
          <n-input-number v-model:value="extra_paid_diamond" :min="0">
            <template #prefix>???????????????</template>
          </n-input-number>
          <n-divider />
          <n-button @click="computeDiamonds">
            ????????????
          </n-button>
            ????????????????????????{{ total_free_diamond }}
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
            content.append("                <template #prefix>??????????????????</template>\n")
            content.append("              </n-input-number>\n")
            content.append("              <n-input-number v-model:value=\"{}\" :min=\"0\">\n".format(gacha_info[key]["stars_key"]))
            content.append("                <template #prefix>?????????????????????</template>\n")
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
