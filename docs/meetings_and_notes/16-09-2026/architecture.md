# A. Study(Dev)

1. Công nghệ: Fastapi + Angular + DB(NeonDB + PostGreDB)
2. Workflow:
   1. Clients ===Reqs==> Server(Local-FE-angular(**http://localhost:5137**)))
   2. Server(**Local:5137**) ===>Res(FE-Angular-code-apps/study-client)===> Clients
   3. Clients(Angular-FE) ===> Reqs ===> Server(Be-fastapi: 3001)
   4. Server(3001) ===>Analist data===> Reqs===>DB(Neon)
   5. DB(Neon)===> Res ===> Server(3001)===> Res ===> Clients(Angular-fe)

# B. Work(Dev)

1. Web: tương tự Study
2. mobile:
   1. client(flutter-UI) ===> data ===> clients(controller) ===> Reqs ===> DB(Neon)
   2. DB(Neon) === Res ===> clients(controller) ===> clients(UI)
