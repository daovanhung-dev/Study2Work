import { Global, Module, type DynamicModule } from "@nestjs/common";

import { loadWorkEnvironment, WORK_ENV, type WorkEnvironment } from "./env.js";

@Global()
@Module({})
export class WorkConfigModule {
  static forRoot(environment?: WorkEnvironment): DynamicModule {
    return {
      module: WorkConfigModule,
      providers: [
        {
          provide: WORK_ENV,
          useValue: environment ?? loadWorkEnvironment(),
        },
      ],
      exports: [WORK_ENV],
    };
  }
}
