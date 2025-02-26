<template>
  <q-page class="q-pa-md">
    <!-- Table Component -->
    <ArticleTable :articles="articles" @edit="editArticle" @delete="deleteArticle" />

    <!-- Popup Form -->
    <ArticleForm v-model:show="showForm" :article="selectedArticle" @save="saveArticle" />

    <!-- Button -->
    <div class="row justify-center q-mt-md">
      <q-btn 
        label="Add Article" 
        color="primary" 
        @click="showForm = true"
        size="lg"
        class="q-px-lg q-py-sm"
      />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from 'boot/axios';
import { useQuasar } from "quasar";
import ArticleTable from 'components/ArticleTable.vue';
import ArticleForm from 'components/ArticleForm.vue';

const $q = useQuasar();

interface Article {
  id?: number;
  title: string;
  content: string;
  release_date: string;
}

const articles = ref<Article[]>([]);
const showForm = ref(false);
const selectedArticle = ref<Article | null>(null);

const fetchArticles = async () => {
  try {
    const response = await api.get("/api/articles");
    articles.value = response.data;
  } catch (error) {
    console.error("Error fetching articles:", error);
    $q.notify({ type: "negative", message: "Failed to load articles." });
  }
};

const saveArticle = async (article: Article) => {
  try {
    if (article.id) {
      await api.put(`/api/articles/${article.id}`, article);
      $q.notify({ type: "positive", message: "Article updated successfully!" });
    } else {
      await api.post("/api/articles", article);
      $q.notify({ type: "positive", message: "Article created successfully!" });
    }
    // Use the void operator to ignore promise as required by ESLint
    void fetchArticles();
    showForm.value = false;
  } catch (error) {
    console.error("Error saving article:", error);
    $q.notify({ type: "negative", message: "Failed to save article." });
  }
};

const deleteArticle = async (id: number) => {
  try {
    await api.delete(`/api/articles/${id}`);
    $q.notify({ type: "positive", message: "Article deleted successfully!" });
    void fetchArticles();
  } catch (error) {
    console.error("Error deleting article:", error);
    $q.notify({ type: "negative", message: "Failed to delete article." });
  }
};

const editArticle = (article: Article) => {
  selectedArticle.value = { ...article };
  showForm.value = true;
};

onMounted(fetchArticles);
</script>
