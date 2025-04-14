<template>
  <div
    class="range-slider"
    data-testid="range-slider"
    @mousedown="onSliderMouseDown"
    @touchstart.passive="onSliderTouchStart"
  >
    <div class="range-slider__track" data-testid="range-slider-track">
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
        data-testid="range-slider-thumb-start"
        :style="{ left: `${position(modelValue[0])}%` }"
        @mousedown="onThumbMouseDown('start', $event)"
        @touchstart.passive="onThumbTouchStart('start', $event)"
      >
        <div class="range-slider__value">
          {{ defaultFormatValue(modelValue[0]) }}
        </div>
      </div>
      <div
        ref="endThumb"
        class="range-slider__thumb"
        data-testid="range-slider-thumb-end"
        :style="{ left: `${position(modelValue[1])}%` }"
        @mousedown="onThumbMouseDown('end', $event)"
        @touchstart.passive="onThumbTouchStart('end', $event)"
      >
        <div class="range-slider__value">
          {{ defaultFormatValue(modelValue[1]) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, computed } from "vue"

  const props = defineProps<{
    /* eslint-disable no-unused-vars */
    modelValue: [Date, Date]
    min?: Date
    max?: Date
    step?: number
    formatValue?: (value: Date) => string
  }>()

  const emit = defineEmits<{
    /* eslint-disable no-unused-vars */
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
    ((value.getTime() - min.value.getTime()) /
      (max.value.getTime() - min.value.getTime())) *
    100

  const roundValue = (value: Date) => {
    const timeFromMin = value.getTime() - min.value.getTime()
    const steppedTime = Math.round(timeFromMin / step.value) * step.value
    const roundedDate = new Date(min.value.getTime() + steppedTime)
    return new Date(
      Math.min(
        max.value.getTime(),
        Math.max(min.value.getTime(), roundedDate.getTime())
      )
    )
  }

  const updateValue = (value: Date) => {
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

  const onSliderMouseDown = (event: MouseEvent) => {
    const track = event.currentTarget as HTMLElement
    if (!track) {
      return
    }
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

  const onSliderTouchStart = (event: TouchEvent) => {
    const touch = event.touches[0]
    const simulatedMouseEvent = new MouseEvent("mousedown", {
      bubbles: true,
      cancelable: true,
      clientX: touch.clientX,
      clientY: touch.clientY,
      button: 0,
    })

    onSliderMouseDown(simulatedMouseEvent)
  }

  const onMouseMove = (event: MouseEvent) => {
    if (!activeThumb.value) return

    const value = getValueFromEvent(event)
    const roundedValue = roundValue(value)

    if (activeThumb.value === "start") {
      emit("update:modelValue", [
        new Date(
          Math.min(roundedValue.getTime(), props.modelValue[1].getTime())
        ),
        props.modelValue[1],
      ])
    } else if (activeThumb.value === "end") {
      emit("update:modelValue", [
        props.modelValue[0],
        new Date(
          Math.max(roundedValue.getTime(), props.modelValue[0].getTime())
        ),
      ])
    }
  }

  const onMouseUp = () => {
    activeThumb.value = null
    emit("end", props.modelValue)
    window.removeEventListener("mousemove", onMouseMove)
    window.removeEventListener("mouseup", onMouseUp)
  }

  const onThumbMouseDown = (thumb: "start" | "end", _: MouseEvent) => {
    activeThumb.value = thumb
    emit("start", props.modelValue)
    window.addEventListener("mousemove", onMouseMove)
    window.addEventListener("mouseup", onMouseUp)
  }

  const onThumbTouchStart = (thumb: "start" | "end", _: TouchEvent) => {
    activeThumb.value = thumb
    emit("start", props.modelValue)

    window.addEventListener("touchmove", onTouchMove)
    window.addEventListener("touchend", onTouchEnd)
  }

  const onTouchMove = (event: TouchEvent) => {
    if (!activeThumb.value) return

    const touch = event.touches[0]
    if (!touch) return

    const value = getValueFromEvent(touch)
    updateValue(value)
  }

  const onTouchEnd = () => {
    activeThumb.value = null
    emit("end", props.modelValue)

    window.removeEventListener("touchmove", onTouchMove)
    window.removeEventListener("touchend", onTouchEnd)
  }

  const getValueFromEvent = (event: MouseEvent | Touch) => {
    const track = startThumb.value?.closest(
      ".range-slider__track"
    ) as HTMLElement

    if (!track) {
      return roundValue(new Date(min.value.getTime()))
    }

    const rect = track.getBoundingClientRect()
    const offset = Math.max(
      0,
      Math.min(1, (event.clientX - rect.left) / rect.width)
    )
    const range = max.value.getTime() - min.value.getTime()
    const value = new Date(min.value.getTime() + offset * range)
    return roundValue(value)
  }

  const defaultFormatValue = (value: Date) => {
    return props.formatValue
      ? props.formatValue(value)
      : `${value.toLocaleDateString()} ${value.toLocaleTimeString()}`
  }
</script>

<style scoped>
  .range-slider {
    position: relative;
    height: 30px;
    width: 75%;
    margin-top: 1.5rem;
    user-select: none;
  }

  .range-slider__track {
    position: relative;
    height: 10px;
    background-color: #e0e0e0;
    border-radius: 2px;
    cursor: pointer;
  }

  .range-slider__range {
    position: absolute;
    height: 100%;
    background-color: #0d1d47;
    border-radius: 2px;
  }

  .range-slider__thumb {
    position: absolute;
    top: 50%;
    width: 20px;
    height: 20px;
    background-color: #0d1d47;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    cursor: pointer;
  }

  .range-slider__value {
    position: absolute;
    top: 24px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #0d1d47;
    color: #ffffff;
    font-size: 12px;
    padding: 2px 6px;
    border-radius: 4px;
    white-space: pre;
  }
</style>
