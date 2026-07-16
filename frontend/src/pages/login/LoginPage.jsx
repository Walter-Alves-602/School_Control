import { useState } from "react";
import "../../styles/pages/login.css";

import {
  ArrowEnterIcon,
  Crown,
  EmailIcon,
  EyeOffIcon,
  LockIcon,
} from "../../components/login/LoginIcons";
import BannerLogin from "../../assets/images/inspiracao/BannerAvatar.png";
import Fenix from "../../assets/images/fenix.png";
import { login } from "../../api/authApi";

function PhoenixLogo({ className = "Fenix" }) {
  return (
    <img
      className={className}
      src={Fenix}
      alt="Ilustracao inspirada no universo Infinity"
    />
  );
}

function LoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const token = await login(username, password);
      onLoginSuccess(token);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

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

            <form className="login-form" onSubmit={handleSubmit}>
              <label className="field-group" htmlFor="login">
                <span>LOGIN</span>
                <div className="field-control">
                  <EmailIcon />
                  <input
                    id="login"
                    type="text"
                    placeholder="Digite seu login"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                    required
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
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    required
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

              {error && <p className="login-form__error">{error}</p>}

              <button type="submit" className="submit-button" disabled={loading}>
                <ArrowEnterIcon />
                <span>{loading ? "Entrando..." : "Entrar"}</span>
              </button>
            </form>


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
