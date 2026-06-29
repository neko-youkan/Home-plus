import streamlit as st

from components.ui import show_title
from services.ingredient_service import (
    add_ingredient,
    delete_ingredient,
    get_ingredients_by_recipe,
)
from services.recipe_service import get_all_recipes
from components.ui import show_title

def show_recipe_detail_card():
    with st.container(border=True):
        show_title("recipe_list", "📖", "登録済みテンプレート")

        recipes = get_all_recipes()

        if not recipes:
            st.write("まだテンプレートがありません")
            return

        for recipe in recipes:
            with st.expander(recipe["name"]):
                st.write(f"🍚 主食　{recipe['staple'] or '未入力'}")
                st.write(f"🐟 主菜　{recipe['main_dish'] or '未入力'}")
                st.write(f"🥗 副菜　{recipe['side_dish'] or '未入力'}")
                st.write(f"🥣 汁物　{recipe['soup'] or '未入力'}")

                st.divider()

                st.write("🥕 **食材**")

                ingredients = get_ingredients_by_recipe(recipe["id"])

                if not ingredients:
                    st.write("食材はまだ登録されていません")
                else:
                    for ingredient in ingredients:
                        col1, col2 = st.columns([4, 1])

                        with col1:
                            st.write(f"□ {ingredient['ingredient_name']}")

                        with col2:
                            if st.button(
                                "🗑",
                                key=f"delete_ingredient_{ingredient['id']}",
                            ):
                                delete_ingredient(ingredient["id"])
                                st.success("食材を削除しました")
                                st.rerun()

                ingredient_name = st.text_input(
                    "食材を追加",
                    placeholder="例）玉ねぎ",
                    key=f"ingredient_name_{recipe['id']}",
                )

                if st.button(
                    "➕ 食材追加",
                    use_container_width=True,
                    key=f"add_ingredient_{recipe['id']}",
                ):
                    result = add_ingredient(recipe["id"], ingredient_name)

                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])