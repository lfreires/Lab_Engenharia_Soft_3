from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk


class TkApp:
    def __init__(self, auth_ctrl, book_ctrl, cart_ctrl, order_ctrl) -> None:
        self._auth = auth_ctrl
        self._books = book_ctrl
        self._cart_ctrl = cart_ctrl
        self._orders = order_ctrl

        self._current_user: str | None = None
        self._cart_id: str | None = None
        self._raw_cart_total: float = 0.0

        self._root = tk.Tk()
        self._root.title("Livraria")
        self._root.geometry("960x640")
        self._root.resizable(False, False)

        self._show_login()

    def run(self) -> None:
        self._root.mainloop()

    def _clear(self) -> None:
        for widget in self._root.winfo_children():
            widget.destroy()

    # ── Tela de login ──────────────────────────────────────────────────────

    def _show_login(self) -> None:
        self._clear()
        self._current_user = None
        self._cart_id = None

        frame = tk.Frame(self._root, padx=60, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Livraria", font=("Helvetica", 28, "bold")).pack(pady=(0, 30))

        form = tk.Frame(frame)
        form.pack()

        tk.Label(form, text="Usuário", anchor="w").grid(row=0, column=0, sticky="w")
        self._login_user = tk.StringVar()
        user_entry = tk.Entry(form, textvariable=self._login_user, width=28)
        user_entry.grid(row=1, column=0, pady=(2, 12))
        user_entry.focus()

        tk.Label(form, text="Senha", anchor="w").grid(row=2, column=0, sticky="w")
        self._login_pass = tk.StringVar()
        pass_entry = tk.Entry(form, textvariable=self._login_pass, show="*", width=28)
        pass_entry.grid(row=3, column=0, pady=(2, 20))
        pass_entry.bind("<Return>", lambda _e: self._do_login())

        tk.Button(form, text="Entrar", command=self._do_login,
                  width=26, bg="#2980b9", fg="white", relief="flat", pady=6).grid(row=4, column=0)

        sep = tk.Frame(frame)
        sep.pack(pady=(16, 0))
        tk.Label(sep, text="Nao tem uma conta?", fg="#666").pack(side="left")
        link = tk.Label(sep, text=" Criar conta", fg="#2980b9", cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda _e: self._show_register())

    def _do_login(self) -> None:
        u = self._login_user.get().strip()
        p = self._login_pass.get().strip()
        if not u or not p:
            messagebox.showwarning("Atenção", "Preencha usuário e senha.")
            return
        try:
            if self._auth.login(u, p):
                self._current_user = u
                self._show_main()
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ── Tela de registro ───────────────────────────────────────────────────

    def _show_register(self) -> None:
        self._clear()

        frame = tk.Frame(self._root, padx=60, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Criar conta", font=("Helvetica", 24, "bold")).pack(pady=(0, 6))
        tk.Label(frame, text="Preencha os dados abaixo para se cadastrar.",
                 fg="#666").pack(pady=(0, 24))

        form = tk.Frame(frame)
        form.pack()

        tk.Label(form, text="Usuário", anchor="w").grid(row=0, column=0, sticky="w")
        self._reg_user = tk.StringVar()
        user_entry = tk.Entry(form, textvariable=self._reg_user, width=30)
        user_entry.grid(row=1, column=0, pady=(2, 12))
        user_entry.focus()

        tk.Label(form, text="Senha", anchor="w").grid(row=2, column=0, sticky="w")
        self._reg_pass = tk.StringVar()
        tk.Entry(form, textvariable=self._reg_pass, show="*", width=30).grid(row=3, column=0, pady=(2, 12))

        tk.Label(form, text="Confirmar senha", anchor="w").grid(row=4, column=0, sticky="w")
        self._reg_pass2 = tk.StringVar()
        confirm_entry = tk.Entry(form, textvariable=self._reg_pass2, show="*", width=30)
        confirm_entry.grid(row=5, column=0, pady=(2, 20))
        confirm_entry.bind("<Return>", lambda _e: self._do_register())

        tk.Button(form, text="Criar conta", command=self._do_register,
                  width=28, bg="#27ae60", fg="white", relief="flat", pady=6).grid(row=6, column=0)

        sep = tk.Frame(frame)
        sep.pack(pady=(16, 0))
        tk.Label(sep, text="Ja tem uma conta?", fg="#666").pack(side="left")
        link = tk.Label(sep, text=" Fazer login", fg="#2980b9", cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda _e: self._show_login())

    def _do_register(self) -> None:
        u = self._reg_user.get().strip()
        p = self._reg_pass.get().strip()
        p2 = self._reg_pass2.get().strip()

        if not u or not p or not p2:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        if p != p2:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
        try:
            self._auth.register_user(u, p)
            messagebox.showinfo("Conta criada!", f"Usuário '{u}' cadastrado com sucesso!")
            self._show_login()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    # ── Tela principal ─────────────────────────────────────────────────────

    def _show_main(self) -> None:
        self._clear()
        cart = self._cart_ctrl.create_cart()
        self._cart_id = cart.id

        # Cabeçalho
        hdr = tk.Frame(self._root, bg="#2c3e50", pady=6)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Livraria", bg="#2c3e50", fg="white",
                 font=("Helvetica", 13, "bold")).pack(side="left", padx=14)
        tk.Label(hdr, text=f"Ola, {self._current_user}", bg="#2c3e50", fg="#bdc3c7",
                 font=("Helvetica", 11)).pack(side="left", padx=8)
        tk.Button(hdr, text="Sair", command=self._show_login,
                  bg="#c0392b", fg="white", relief="flat", padx=10).pack(side="right", padx=14, pady=3)

        # Corpo
        body = tk.Frame(self._root)
        body.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_books_panel(body)
        self._build_cart_panel(body)

        self._refresh_books()

    # ── Painel de livros (esquerda) ────────────────────────────────────────

    def _build_books_panel(self, parent: tk.Frame) -> None:
        left = tk.Frame(parent)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Lista de livros
        list_frame = tk.LabelFrame(left, text="Livros disponiveis", padx=6, pady=6)
        list_frame.pack(fill="both", expand=True)

        cols = ("title", "price", "stock")
        self._book_tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=11)
        self._book_tree.heading("title", text="Titulo")
        self._book_tree.heading("price", text="Preco")
        self._book_tree.heading("stock", text="Estoque")
        self._book_tree.column("title", width=230)
        self._book_tree.column("price", width=90, anchor="center")
        self._book_tree.column("stock", width=70, anchor="center")

        sb = ttk.Scrollbar(list_frame, orient="vertical", command=self._book_tree.yview)
        self._book_tree.configure(yscrollcommand=sb.set)
        self._book_tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Adicionar ao carrinho
        act = tk.Frame(left, pady=4)
        act.pack(fill="x")
        tk.Label(act, text="Qtd:").pack(side="left")
        self._qty_var = tk.IntVar(value=1)
        tk.Spinbox(act, from_=1, to=99, textvariable=self._qty_var, width=5).pack(side="left", padx=4)
        tk.Button(act, text="Adicionar ao carrinho", command=self._add_to_cart,
                  bg="#27ae60", fg="white", relief="flat", padx=8).pack(side="left")

        # Cadastrar livro
        form_frame = tk.LabelFrame(left, text="Cadastrar livro", padx=6, pady=6)
        form_frame.pack(fill="x")

        fg = tk.Frame(form_frame)
        fg.pack(fill="x")

        self._new_book_vars: dict[str, tk.StringVar] = {}
        for i, (lbl, key) in enumerate([("Titulo", "title"), ("Preco", "price"), ("Estoque", "stock")]):
            tk.Label(fg, text=lbl, width=7, anchor="w").grid(row=i, column=0, sticky="w", pady=2)
            var = tk.StringVar()
            self._new_book_vars[key] = var
            tk.Entry(fg, textvariable=var, width=26).grid(row=i, column=1, pady=2, sticky="w")

        tk.Button(form_frame, text="Cadastrar livro", command=self._create_book,
                  bg="#8e44ad", fg="white", relief="flat", padx=8).pack(pady=(6, 0))

    # ── Painel do carrinho (direita) ───────────────────────────────────────

    def _build_cart_panel(self, parent: tk.Frame) -> None:
        right = tk.Frame(parent, width=290)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        cart_frame = tk.LabelFrame(right, text="Carrinho", padx=6, pady=6)
        cart_frame.pack(fill="both", expand=True)

        cols = ("item", "subtotal")
        self._cart_tree = ttk.Treeview(cart_frame, columns=cols, show="headings", height=9)
        self._cart_tree.heading("item", text="Item")
        self._cart_tree.heading("subtotal", text="Subtotal")
        self._cart_tree.column("item", width=175)
        self._cart_tree.column("subtotal", width=80, anchor="center")
        self._cart_tree.pack(fill="both", expand=True)

        self._total_var = tk.StringVar(value="Total: R$ 0,00")
        tk.Label(cart_frame, textvariable=self._total_var,
                 font=("Helvetica", 10, "bold"), anchor="e").pack(fill="x", pady=(4, 0))

        tk.Button(cart_frame, text="Remover item selecionado", command=self._remove_from_cart,
                  bg="#c0392b", fg="white", relief="flat", pady=3).pack(fill="x", pady=(6, 0))

        # Pagamento
        pay_frame = tk.LabelFrame(right, text="Pagamento", padx=6, pady=6)
        pay_frame.pack(fill="x", pady=(8, 0))

        self._payment_var = tk.StringVar(value="pix")
        for label, value in [("Pix", "pix"), ("Cartao", "card"), ("Dinheiro", "cash")]:
            tk.Radiobutton(pay_frame, text=label, variable=self._payment_var,
                           value=value).pack(anchor="w")

        tk.Label(pay_frame, text="Cupom de desconto:", anchor="w").pack(anchor="w", pady=(8, 0))
        self._coupon_var = tk.StringVar()
        tk.Entry(pay_frame, textvariable=self._coupon_var, width=22).pack(fill="x", pady=(2, 0))
        self._coupon_status_var = tk.StringVar()
        self._coupon_status_label = tk.Label(
            pay_frame, textvariable=self._coupon_status_var,
            font=("Helvetica", 9), anchor="w", wraplength=240,
        )
        self._coupon_status_label.pack(fill="x", pady=(2, 0))
        self._coupon_var.trace_add("write", lambda *_: self._on_coupon_change())

        tk.Button(right, text="Finalizar pedido", command=self._checkout,
                  bg="#27ae60", fg="white", font=("Helvetica", 10, "bold"),
                  relief="flat", pady=8).pack(fill="x", pady=(10, 0))

    # ── Ações ──────────────────────────────────────────────────────────────

    def _refresh_books(self) -> None:
        self._book_tree.delete(*self._book_tree.get_children())
        for book in self._books.list_books():
            self._book_tree.insert("", "end", iid=book.id,
                                   values=(book.title, f"R$ {book.price:.2f}", book.stock))

    def _refresh_cart(self) -> None:
        self._cart_tree.delete(*self._cart_tree.get_children())
        cart = self._cart_ctrl.get_cart(self._cart_id)
        for item in cart.items:
            self._cart_tree.insert("", "end", iid=item.book_id,
                                   values=(f"{item.title} x{item.quantity}",
                                           f"R$ {item.subtotal:.2f}"))
        self._raw_cart_total = cart.total
        self._apply_coupon_preview()

    def _on_coupon_change(self) -> None:
        self._apply_coupon_preview()

    def _apply_coupon_preview(self) -> None:
        code = self._coupon_var.get().strip()
        if not code:
            self._total_var.set(f"Total: R$ {self._raw_cart_total:.2f}")
            self._coupon_status_var.set("")
            return
        try:
            discounted, savings = self._orders.preview_discount(self._raw_cart_total, code)
            self._total_var.set(f"Total: R$ {discounted:.2f}")
            self._coupon_status_var.set(f"Cupom valido! Economia de R$ {savings:.2f}")
            self._coupon_status_label.config(fg="#27ae60")
        except Exception as e:
            self._total_var.set(f"Total: R$ {self._raw_cart_total:.2f}")
            self._coupon_status_var.set(str(e))
            self._coupon_status_label.config(fg="#c0392b")

    def _add_to_cart(self) -> None:
        selected = self._book_tree.focus()
        if not selected:
            messagebox.showwarning("Atencao", "Selecione um livro.")
            return
        try:
            self._cart_ctrl.add_book(self._cart_id, selected, self._qty_var.get())
            self._refresh_cart()
        except (ValueError, KeyError) as e:
            messagebox.showerror("Erro", str(e))

    def _remove_from_cart(self) -> None:
        selected = self._cart_tree.focus()
        if not selected:
            messagebox.showwarning("Atencao", "Selecione um item do carrinho.")
            return
        try:
            self._cart_ctrl.remove_book(self._cart_id, selected)
            self._refresh_cart()
        except (ValueError, KeyError) as e:
            messagebox.showerror("Erro", str(e))

    def _create_book(self) -> None:
        v = self._new_book_vars
        title = v["title"].get().strip()
        price_str = v["price"].get().strip()
        stock_str = v["stock"].get().strip()

        if not all([title, price_str, stock_str]):
            messagebox.showwarning("Atencao", "Preencha todos os campos.")
            return
        try:
            price = float(price_str.replace(",", "."))
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Erro", "Preco deve ser numero e estoque deve ser inteiro.")
            return
        try:
            self._books.create_book(title, price, stock)
            for var in v.values():
                var.set("")
            self._refresh_books()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _checkout(self) -> None:
        cart = self._cart_ctrl.get_cart(self._cart_id)
        if not cart.items:
            messagebox.showwarning("Atencao", "O carrinho esta vazio.")
            return

        method = self._payment_var.get()
        method_label = {"pix": "Pix", "card": "Cartao", "cash": "Dinheiro"}[method]
        coupon_code = self._coupon_var.get().strip() or None

        confirm_msg = f"Finalizar via {method_label}?\nTotal: R$ {cart.total:.2f}"
        if coupon_code:
            confirm_msg += f"\nCupom: {coupon_code}"

        if not messagebox.askyesno("Confirmar pedido", confirm_msg):
            return
        try:
            order = self._orders.checkout(self._cart_id, payment_method=method, coupon_code=coupon_code)
            info_msg = (
                f"Pedido criado com sucesso!\n"
                f"Total: R$ {order.total:.2f}\n"
                f"Pagamento: {order.payment.method} — {order.payment.status}"
            )
            discount = cart.total - order.total
            if discount > 0.001:
                info_msg += f"\nDesconto aplicado: R$ {discount:.2f}"
            messagebox.showinfo("Pedido realizado!", info_msg)
            new_cart = self._cart_ctrl.create_cart()
            self._cart_id = new_cart.id
            self._coupon_var.set("")
            self._coupon_status_var.set("")
            self._refresh_cart()
            self._refresh_books()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
