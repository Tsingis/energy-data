<template>
  <div
    class="range-slider"
    @mousedown="onSliderMouseDown"
    @touchstart="onSliderTouchStart"
  >
    <div class="range-slider__track">
      <div
        class="range-slider__range"
        :style="{
          left: `${position(modelValue[0])}%`,
          width: `${position(modelValue[1]) - position(modelValue[0])}%`,
        }"
      ></div>
      <div
        ref="startThumb"
        class="range-slider__thumb"
        :style="{ left: `${position(modelValue[0])}%` }"
        @mousedown="onThumbMouseDown('start', $event)"
        @touchstart="onThumbTouchStart('start', $event)"
      >
        <div class="range-slider__value">
          {{ formatValue(modelValue[0]) }}
        </div>
      </div>
      <div
        ref="endThumb"
        class="range-slider__thumb"
        :style="{ left: `${position(modelValue[1])}%` }"
        @mousedown="onThumbMouseDown('end', $event)"
        @touchstart="onThumbTouchStart('end', $event)"
      >
        <div class="range-slider__value">
          {{ formatValue(modelValue[1]) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, computed } from "vue"
  import { format, addMilliseconds, differenceInMilliseconds } from "date-fns"

  const props = defineProps<{
    modelValue: [Date, Date]
    min?: Date
    max?: Date
    step?: number
    formatValue?: (value: Date) => string
  }>()

  const emit = defineEmits<{
    (e: "update:modelValue", value: [Date, Date]): void
    (e: "start", value: [Date, Date]): void
    (e: "end", value: [Date, Date]): void
  }>()

  const min = computed(() => props.min ?? new Date(0))
  const max = computed(() => props.max ?? new Date())
  const step = computed(() => props.step ?? 3600000)

  const startThumb = ref<HTMLElement | null>(null)
  const endThumb = ref<HTMLElement | null>(null)
  const activeThumb = ref<"start" | "end" | null>(null)

  const position = (value: Date) =>
    (differenceInMilliseconds(value, min.value) /
      differenceInMilliseconds(max.value, min.value)) *
    100

  function roundValue(value: Date) {
    const timeFromMin = differenceInMilliseconds(value, min.value)
    const steppedTime = Math.round(timeFromMin / step.value) * step.value
    const roundedDate = addMilliseconds(min.value, steppedTime)
    return new Date(
      Math.min(
        max.value.getTime(),
        Math.max(min.value.getTime(), roundedDate.getTime())
      )
    )
  }

  function updateValue(value: Date) {
    if (activeThumb.value === "start") {
      emit("update:modelValue", [
        new Date(
          Math.min(roundValue(value).getTime(), props.modelValue[1].getTime())
        ),
        props.modelValue[1],
      ])
    } else if (activeThumb.value === "end") {
      emit("update:modelValue", [
        props.modelValue[0],
        new Date(
          Math.max(roundValue(value).getTime(), props.modelValue[0].getTime())
        ),
      ])
    }
  }

  function onSliderMouseDown(event: MouseEvent) {
    const value = getValueFromEvent(event)
    const closestThumb =
      Math.abs(value.getTime() - props.modelValue[0].getTime()) <
      Math.abs(value.getTime() - props.modelValue[1].getTime())
        ? "start"
        : "end"
    activeThumb.value = closestThumb
    emit("start", props.modelValue)
    updateValue(value)
    window.addEventListener("mousemove", onMouseMove)
    window.addEventListener("mouseup", onMouseUp)
  }

  function onSliderTouchStart(event: TouchEvent) {
    onSliderMouseDown(event.touches[0])
  }

  function onMouseMove(event: MouseEvent) {
    const value = getValueFromEvent(event)
    updateValue(value)
  }

  function onMouseUp() {
    activeThumb.value = null
    emit("end", props.modelValue)
    window.removeEventListener("mousemove", onMouseMove)
    window.removeEventListener("mouseup", onMouseUp)
  }

  function onThumbMouseDown(thumb: "start" | "end", event: MouseEvent) {
    event.stopPropagation()
    activeThumb.value = thumb
    emit("start", props.modelValue)
    window.addEventListener("mousemove", onMouseMove)
    window.addEventListener("mouseup", onMouseUp)
  }

  function onThumbTouchStart(thumb: "start" | "end", event: TouchEvent) {
    onThumbMouseDown(thumb, event.touches[0] as any)
  }

  function getValueFromEvent(event: MouseEvent | Touch) {
    const track = (event.target as HTMLElement).closest(
      ".range-slider__track"
    ) as HTMLElement
    const rect = track.getBoundingClientRect()
    const offset = (event.clientX - rect.left) / rect.width
    const range = differenceInMilliseconds(max.value, min.value)
    const value = addMilliseconds(min.value, offset * range)
    return roundValue(value)
  }

  const formatValue = (value: Date) => {
    return props.formatValue
      ? props.formatValue(value)
      : format(value, "yyyy-MM-dd HH:mm")
  }
</script>

<style scoped>
  .range-slider {
    position: relative;
    height: 20px;
    user-select: none;
  }

  .range-slider__track {
    position: relative;
    height: 4px;
    background-color: #e0e0e0;
    border-radius: 2px;
  }

  .range-slider__range {
    position: absolute;
    height: 100%;
    background-color: #6200ea;
    border-radius: 2px;
  }

  .range-slider__thumb {
    position: absolute;
    top: 50%;
    width: 16px;
    height: 16px;
    background-color: #6200ea;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    cursor: pointer;
  }

  .range-slider__value {
    position: absolute;
    top: -24px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #6200ea;
    color: #ffffff;
    font-size: 12px;
    padding: 2px 6px;
    border-radius: 4px;
    white-space: nowrap;
  }
</style>
