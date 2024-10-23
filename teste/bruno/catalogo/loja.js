if (document.readyState == 'loading') {
  document.addEventListener('DOMContentLoaded', ready);
} else {
  ready();
}

let totalAmount = "0,00";

function ready() {
  // Botão remover produto
  const removeCartProductButtons = document.getElementsByClassName("remove-product-button");
  for (let i = 0; i < removeCartProductButtons.length; i++) {
    removeCartProductButtons[i].addEventListener("click", removeProduct);
  }

  // Mudança valor dos inputs
  const quantityInputs = document.getElementsByClassName("product-qtd-input");
  for (let i = 0; i < quantityInputs.length; i++) {
    quantityInputs[i].addEventListener("change", checkIfInputIsNull);
  }

  // Botão add produto ao carrinho
  const addToCartButtons = document.getElementsByClassName("add-to-cart");
  for (let i = 0; i < addToCartButtons.length; i++) {
    addToCartButtons[i].addEventListener("click", addProductToCart);
  }

  // Botão comprar
  const purchaseButton = document.getElementsByClassName("purchase-button")[0];
  purchaseButton.addEventListener("click", makePurchase);
}

function removeProduct(event) {
  event.target.parentElement.parentElement.remove();
  updateTotal();
}

function checkIfInputIsNull(event) {
  if (event.target.value === "0") {
    event.target.parentElement.parentElement.remove();
  }
  updateTotal();
}

function addProductToCart(event) {
  const button = event.target;
  const productInfos = button.closest('.card-item');
  const productName = productInfos.getElementsByClassName("product-title")[0].innerText;
  const productPrice = productInfos.getElementsByClassName("product-price")[0].innerText;

  const productsCartNames = document.getElementsByClassName("cart-product-title");
  for (let i = 0; i < productsCartNames.length; i++) {
    if (productsCartNames[i].innerText === productName) {
      productsCartNames[i].parentElement.parentElement.getElementsByClassName("product-qtd-input")[0].value++;
      updateTotal();
      return;
    }
  }

  let newCartProduct = document.createElement("tr");
  newCartProduct.classList.add("cart-product");

  newCartProduct.innerHTML =
    `
      <td class="product-identification">
        <strong class="cart-product-title">${productName}</strong>
      </td>
      <td>
        <span class="cart-product-price">${productPrice}</span>
      </td>
      <td>
        <input type="number" value="1" min="0" class="product-qtd-input">
        <button type="button" class="remove-product-button">Remover</button>
      </td>
    `;

  const tableBody = document.querySelector(".cart-table tbody");
  tableBody.append(newCartProduct);
  updateTotal();

  newCartProduct.getElementsByClassName("remove-product-button")[0].addEventListener("click", removeProduct);
  newCartProduct.getElementsByClassName("product-qtd-input")[0].addEventListener("change", checkIfInputIsNull);
}


function updateTotal() {
  const cartProducts = document.getElementsByClassName("cart-product");
  totalAmount = 0;

  for (let i = 0; i < cartProducts.length; i++) {
    const productPrice = parseFloat(cartProducts[i].getElementsByClassName("cart-product-price")[0].innerText.replace("R$", "").replace(",", "."));
    const productQuantity = parseInt(cartProducts[i].getElementsByClassName("product-qtd-input")[0].value);

    totalAmount += productPrice * productQuantity;
  }

  totalAmount = totalAmount.toFixed(2);
  totalAmount = totalAmount.replace(".", ",");
  document.querySelector(".cart-total-container span").innerText = "R$" + totalAmount;
}
