import "./globals.css";

export const metadata = {
  title: "Free eCommerce Product Page SEO Checker | Audit Your Store",
  description: "Check your Shopify or WooCommerce product page SEO instantly. Get a free score on title tags, meta descriptions, H1 tags, and image alt text.",
  keywords: ["eCommerce SEO", "SEO Checker", "Product Page Audit", "Shopify SEO tool", "Free SEO Audit"],
  openGraph: {
    title: "eCommerce Product Page SEO Checker",
    description: "Boost your store's ranking with our free SEO audit tool.",
    type: "website",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="antialiased font-sans bg-slate-50 text-slate-900">
        {children}
      </body>
    </html>
  );
}