import { ref } from "vue"

export function useFetchData<T>(fetchFunction: () => Promise<T>) {
  const data = ref<T | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchData = async () => {
    loading.value = true
    error.value = null

    try {
      data.value = await fetchFunction()
    } catch (err) {
      console.log(err)
      setTimeout(fetchData, 5000)
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, fetchData }
}
