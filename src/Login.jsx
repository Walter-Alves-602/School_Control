import "./style/login.css";
import BannerAvatar from "./assets/inspiracao/BannerAvatar.png";
function TelaLogin() {
  return (
    <>
      <header>
        <nav>
          <h1>Infinty Control</h1>
        </nav>
      </header>

      <section id="formulario">
        <img src={BannerAvatar} alt="Banner Avatar" />

        <form action="" method="get">
          <h1>Bem Vindo de Volta !</h1>
          <p>faça o login para acessar sua conta</p>
          <label htmlFor="">email</label>
          <input type="email" name="" id="emailid" />
          <label htmlFor="">passoword</label>
          <input type="password" name="" id="passoword" />
          
        </form>
      </section>
    </>
  );
}

export default TelaLogin;
