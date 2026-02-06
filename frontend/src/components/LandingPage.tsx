interface LandingPageProps {
  onStartTool: () => void
}

export function LandingPage({ onStartTool }: LandingPageProps) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero Section */}
      <header className="max-w-5xl mx-auto px-4 py-16 text-center">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
          Controlmyentries
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Detectez automatiquement les anomalies dans vos ecritures comptables.
          Gagnez du temps sur vos controles mensuels.
        </p>
        <button
          onClick={onStartTool}
          className="
            inline-flex items-center gap-2
            px-8 py-4 text-lg font-medium
            text-white bg-primary-600 rounded-xl
            hover:bg-primary-700
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2
            transition-colors duration-200
            shadow-lg hover:shadow-xl
            min-h-[56px]
          "
        >
          Essayer gratuitement
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </button>
      </header>

      {/* Features Section */}
      <section className="max-w-5xl mx-auto px-4 py-16" aria-labelledby="features-heading">
        <h2 id="features-heading" className="text-3xl font-bold text-center text-gray-900 mb-12">
          Comment ca marche
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          {/* Step 1 */}
          <div className="text-center p-6">
            <div className="w-16 h-16 mx-auto mb-4 bg-primary-100 rounded-2xl flex items-center justify-center">
              <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              1. Deposez vos fichiers
            </h3>
            <p className="text-gray-600">
              Glissez votre Grand Livre et optionnellement votre baseline pour l'analyse statistique.
            </p>
          </div>

          {/* Step 2 */}
          <div className="text-center p-6">
            <div className="w-16 h-16 mx-auto mb-4 bg-primary-100 rounded-2xl flex items-center justify-center">
              <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              2. Analyse automatique
            </h3>
            <p className="text-gray-600">
              Notre algorithme detecte les disparitions, apparitions, variations et anomalies statistiques.
            </p>
          </div>

          {/* Step 3 */}
          <div className="text-center p-6">
            <div className="w-16 h-16 mx-auto mb-4 bg-primary-100 rounded-2xl flex items-center justify-center">
              <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              3. Rapport Excel
            </h3>
            <p className="text-gray-600">
              Telechargez un rapport detaille avec constats factuels et donnees statistiques.
            </p>
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="bg-gray-50 py-16" aria-labelledby="usecases-heading">
        <div className="max-w-5xl mx-auto px-4">
          <h2 id="usecases-heading" className="text-3xl font-bold text-center text-gray-900 mb-12">
            Pour qui ?
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Controleurs de gestion
              </h3>
              <p className="text-gray-600">
                Automatisez vos controles mensuels et concentrez-vous sur l'analyse des anomalies detectees.
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Directeurs financiers
              </h3>
              <p className="text-gray-600">
                Obtenez une synthese claire des anomalies avec un indice de confiance pour vos decisions.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-5xl mx-auto px-4 py-16 text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Pret a detecter les anomalies ?
        </h2>
        <p className="text-gray-600 mb-8">
          Aucune inscription requise. Vos donnees ne sont pas conservees.
        </p>
        <button
          onClick={onStartTool}
          className="
            inline-flex items-center gap-2
            px-8 py-4 text-lg font-medium
            text-white bg-primary-600 rounded-xl
            hover:bg-primary-700
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2
            transition-colors duration-200
            min-h-[56px]
          "
        >
          Commencer maintenant
        </button>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="max-w-5xl mx-auto px-4 text-center text-sm text-gray-500">
          <p>Controlmyentries - Outil de detection d'anomalies budgetaires</p>
          <p className="mt-2">
            Aide a la detection, pas certificat d'absence d'anomalie.
          </p>
        </div>
      </footer>
    </div>
  )
}
