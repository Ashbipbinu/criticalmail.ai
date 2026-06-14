import seaborn as sns
import matplotlib.pyplot as plt
import os

from wordcloud import WordCloud


class Data_VIsualization:
    def __init__(self):
        pass

    def count_class(self, processed_data, fig_location, fig_name):
        data = processed_data["email_criticality"].value_counts().sort_index()
        data.plot(kind="bar", color="skyblue")

        plt.grid(True, linestyle="--", alpha=0.6)
        plt.xlabel("Classes")
        plt.ylabel("Counts")
        plt.title("Counts of each classes")
        save_loc = os.path.join(fig_location, fig_name)
        plt.savefig(save_loc)
        return

    def len_vs_class(self, df_refined, fig_location, fig_name):
        df_refined["word_length"] = df_refined["message_body_tokens"].apply(
            len)

        plt.figure(figsize=(6, 4))
        sns.histplot(y="word_length", x="email_criticality", data=df_refined)

        plt.xlabel("Class")
        plt.ylabel("Length")
        plt.title("Length of words vs Class")
        plt.tight_layout()

        save_loc = os.path.join(fig_location, fig_name)
        plt.savefig(save_loc)

        return

    def words_cloud(self, df_refined, fig_location, fig_name):
        class_1_words = " ".join(
            [
                " ".join(tokens)
                for tokens in df_refined[df_refined["email_criticality"] == 1][
                    "message_body_tokens"
                ]
            ]
        )

        if class_1_words.strip():
            word_cloud_1 = WordCloud(
                width=800, height=400, background_color="white",
                colormap="magma"
            ).generate(class_1_words)

            plt.figure(figsize=(10, 5))
            plt.imshow(word_cloud_1, interpolation="bilinear")
            plt.title("Most Repeating Words in Class 1 (High Criticality)",
                      fontsize=16)
            plt.axis("off")
            plt.tight_layout()

            save_location = os.path.join(fig_location, fig_name)
            plt.savefig(save_location)
