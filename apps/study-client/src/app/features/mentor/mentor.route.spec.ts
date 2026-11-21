import { routes } from '../../app.routes';
import { mentorRoutes } from './mentor.route';

describe('Mentor routes', () => {
  const screens = new Map(
    (mentorRoutes[0]?.children ?? [])
      .filter((route) => typeof route.data?.['screenId'] === 'string')
      .map((route) => [route.data?.['screenId'] as string, route.data?.['apiIds'] as number[]]),
  );

  it('registers all 18 Mentor screens with their server API IDs', () => {
    expect(screens.size).toBe(18);
    expect(screens.get('ME-01')).toEqual([46, 54, 58]);
    expect(screens.get('ME-02')).toEqual([46]);
    expect(screens.get('ME-03')).toEqual([46, 49, 65]);
    expect(screens.get('ME-04')).toEqual([34, 46, 47]);
    expect(screens.get('ME-05')).toEqual([48]);
    expect(screens.get('ME-06')).toEqual([49]);
    expect(screens.get('ME-07')).toEqual([49, 50, 51]);
    expect(screens.get('ME-08')).toEqual([49, 52, 53]);
    expect(screens.get('ME-09')).toEqual([54]);
    expect(screens.get('ME-10')).toEqual([55, 56, 57]);
    expect(screens.get('ME-11')).toEqual([58]);
    expect(screens.get('ME-12')).toEqual([59, 60, 61]);
    expect(screens.get('ME-13')).toEqual([46, 62]);
    expect(screens.get('ME-14')).toEqual([62, 63]);
    expect(screens.get('ME-15')).toEqual([64]);
    expect(screens.get('ME-16')).toEqual([65]);
    expect(screens.get('ME-17')).toEqual([67]);
    expect(screens.get('ME-18')).toEqual([66]);
  });

  it('mounts the Mentor group through the lazy app route', () => {
    expect(routes.some((route) => route.path === 'mentor' && !!route.loadChildren)).toBe(true);
  });

  it('does not assign generic operation polling API #18 to ME-15', () => {
    expect(screens.get('ME-15')).toEqual([64]);
  });
});
