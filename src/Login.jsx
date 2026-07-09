import "./style/login.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBrave,
  faGithub,
  faMicrosoft,
} from "@fortawesome/free-brands-svg-icons";
import BannerLogin from "./assets/inspiracao/bannerAvatar.png";
import Fenix from "./assets/fenix.png";

function PhoenixLogo({ className = "Fenix" }) {
  return (
    <img
      className={className}
      src={Fenix}
      alt="Ilustracao inspirada no universo Infinity"
    />
  );
}

function EmailIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" fill="none">
      <path
        d="M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4Z"
        stroke="currentColor"
        strokeWidth="1.8"
      />
      <path
        d="M4.5 19a7.5 7.5 0 0 1 15 0"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
      />
    </svg>
  );
}

function LockIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" fill="none">
      <path
        d="M7 11V8a5 5 0 0 1 10 0v3"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
      />
      <rect
        x="5"
        y="11"
        width="14"
        height="10"
        rx="2"
        stroke="currentColor"
        strokeWidth="1.8"
      />
      <path
        d="M12 15v2"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
      />
    </svg>
  );
}

function EyeOffIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" fill="none">
      <path
        d="M3 3l18 18M10.6 10.7a2 2 0 0 0 2.7 2.7M9.9 5.1A10.9 10.9 0 0 1 12 5c5.2 0 9.2 4.4 10 6.9a11.8 11.8 0 0 1-3 4.1M6.2 6.3A12.8 12.8 0 0 0 2 11.9C2.8 14.4 6.8 18.8 12 18.8c1.3 0 2.6-.3 3.8-.8"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function ArrowEnterIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" fill="none">
      <path
        d="M13 6l5 6-5 6"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M6 12h12"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <path
        d="M6 5v14"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  );
}

function Crown() {
  return (
    <span className="crown-mark" aria-hidden="true">
      ♛
    </span>
  );
}

function TelaLogin() {
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

export default TelaLogin;
