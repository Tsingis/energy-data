import { ref } from "vue"

export function useFetchData<T>(fetchFunction: () => Promise<T>) {
  const data = ref<T | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchData = async () => {
    if (loading.value) return

    loading.value = true
    error.value = null

    const tryFetch = async () => {
      try {
        data.value = await fetchFunction()
        loading.value = false
      } catch (err) {
        console.error(err)
        error.value = (err as Error).message || "Unknown error"
        setTimeout(() => {
          tryFetch()
        }, 5000)
      }
    }

    tryFetch()
  }

  return { data, loading, error, fetchData }
}
