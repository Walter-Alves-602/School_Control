import "../../styles/pages/login.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBrave,
  faGithub,
  faMicrosoft,
} from "@fortawesome/free-brands-svg-icons";
import {
  ArrowEnterIcon,
  Crown,
  EmailIcon,
  EyeOffIcon,
  LockIcon,
} from "../../components/login/LoginIcons";
import BannerLogin from "../../assets/images/inspiracao/BannerAvatar.png";
import Fenix from "../../assets/images/fenix.png";

function PhoenixLogo({ className = "Fenix" }) {
  return (
    <img
      className={className}
      src={Fenix}
      alt="Ilustracao inspirada no universo Infinity"
    />
  );
}

function LoginPage() {
  return (
    <main className="login-shell">
      <section className="login-card" aria-label="Tela de login Infinity Stock">
        <div className="login-card__art">
          <img
            src={BannerLogin}
            alt="Ilustracao inspirada no universo Infinity"
          />
          <div className="login-card__overlay-copy"></div>
        </div>

        <div className="login-card__panel">
          <div className="panel-brandbar">
            <span>INFINITY SCHOOL</span>
            <Crown />
          </div>

          <div className="panel-content">
            <div className="hero-brand">
              <PhoenixLogo className="hero-brand__icon" />
              <div className="hero-brand__title">
                <span className="hero-brand__line hero-brand__line--light">
                  infinity
                </span>
                <span className="hero-brand__line hero-brand__line--accent">
                  Stock
                </span>
                <p>Contabilizador de estoque em aplicativo!</p>
              </div>
            </div>

            <div className="welcome-copy">
              <h1>Bem-vindo de volta!</h1>
              <p>Faca login para acessar sua conta</p>
            </div>

            <form className="login-form">
              <label className="field-group" htmlFor="email">
                <span>E-MAIL</span>
                <div className="field-control">
                  <EmailIcon />
                  <input
                    id="email"
                    type="email"
                    placeholder="Digite seu e-mail"
                  />
                </div>
              </label>

              <label className="field-group" htmlFor="password">
                <span>SENHA</span>
                <div className="field-control">
                  <LockIcon />
                  <input
                    id="password"
                    type="password"
                    placeholder="Digite sua senha"
                  />
                  <button
                    type="button"
                    className="field-action"
                    aria-label="Mostrar ou ocultar senha"
                  >
                    <EyeOffIcon />
                  </button>
                </div>
              </label>

              <div className="form-options">
                <label className="remember-me" htmlFor="remember">
                  <input id="remember" type="checkbox" />
                  <span>Lembrar de mim</span>
                </label>
                <a href="#recuperar">Esqueceu sua senha?</a>
              </div>

              <button type="submit" className="submit-button">
                <ArrowEnterIcon />
                <span>Entrar</span>
              </button>
            </form>

            <div className="social-login" aria-label="Outras opcoes de login">
              <div className="social-login__divider">
                <span>ou continue com</span>
              </div>

              <div className="social-login__buttons">
                <button type="button" className="social-button">
                  <FontAwesomeIcon
                    icon={faBrave}
                    className="social-button__icon"
                    style={{ color: "rgb(255, 53, 53)" }}
                  />
                  <span>Google</span>
                </button>
                <button type="button" className="social-button">
                  <FontAwesomeIcon
                    icon={faMicrosoft}
                    className="social-button__icon"
                    style={{ color: "rgb(255, 53, 53)" }}
                  />
                  <span>Microsoft</span>
                </button>
                <button type="button" className="social-button">
                  <FontAwesomeIcon
                    icon={faGithub}
                    className="social-button__icon"
                    style={{ color: "rgb(255, 53, 53)" }}
                  />
                  <span>GitHub</span>
                </button>
              </div>
            </div>

            <p className="panel-footer">
              © 2026 DevWizardMaros. Todos os direitos reservados.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}

export default LoginPage;
