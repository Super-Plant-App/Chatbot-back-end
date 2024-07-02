import os
import dotenv
import tiktoken
from openai import OpenAI
from pinecone import Pinecone

dotenv.load_dotenv()


class CureDB:
    def __init__(self) -> None:
        self.namespaceName = "book1"
        pass

    def __initPinecone(self):
        """
        Creates an object of pinecone to access my hosted vectors
        """
        pinecone = Pinecone(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENV"),
        )
        pinecone_index = pinecone.Index(os.getenv("PINECONE_INDEX"))

        return pinecone, pinecone_index

    def __getEmbeddings(
        self, text: str, model: str = "text-embedding-3-large"
    ) -> list[float]:
        """
        Return the Embeddings of a text
        """
        client = OpenAI()

        return client.embeddings.create(input=[text], model=model).data[0].embedding

    def __calcTokens(self, string: str, encoding_name: str = "cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def __displayDocs(self, matching_pages_content):
        sum_text = ""

        for vec_id in matching_pages_content.to_dict()["vectors"].keys():
            page_content = matching_pages_content.to_dict()["vectors"][vec_id][
                "metadata"
            ]["page_content"]
            print("=========================================")
            print(f"ID: {vec_id}")
            print("----")
            print()
            print(page_content)
            print()
            print("=========================================")

            sum_text += page_content + "\n\n\n"

        print(f"Tokens: {self.__calcTokens(sum_text)}")

        return sum_text, self.__calcTokens(sum_text)

    def getCureDocsFromPinecone(self, plantName: str, diseaseName: str, noDocs=1):
        if diseaseName == "healthy":
            return (
                "",
                True,
                0,
            )

        # get Word Embeddings
        query = f"{plantName} plant Managment of {diseaseName} disease?"
        query_vec = self.__getEmbeddings(query)

        # Initilalize pinecone
        _, pinecone_index = self.__initPinecone()

        # Get queries from Pinecone
        query_output = pinecone_index.query(
            vector=query_vec, top_k=noDocs, namespace=self.namespaceName
        )

        # Get relative docs' IDs
        matching_pages_ids = []
        for vec in query_output["matches"]:
            print(vec)
            matching_pages_ids.append(vec["id"])

        # Get relative docs by IDs
        matching_pages_content = pinecone_index.fetch(
            ids=matching_pages_ids, namespace=self.namespaceName
        )

        sum_text, total_tokens = self.__displayDocs(matching_pages_content)

        return sum_text, total_tokens
