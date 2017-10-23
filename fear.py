# pylint: disable=no-member,unused-variable
from math import sqrt

from cymunk import Vec2d
from kivy.factory import Factory
from kivy.logger import Logger  # noqa: F401
from kivy.properties import NumericProperty
from kivent_core.systems.gamesystem import GameSystem

# def debug_F(f):
#     w, h = f.shape
#     from matplotlib import pyplot as plt
#     from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
#     fig = plt.figure()
#     ax = fig.gca(projection='3d')
#     ax.set_zlim(-10, 1000)
#     X = np.arange(w)
#     Y = np.arange(h)
#     X, Y = np.meshgrid(X, Y)
#     ax.plot_wireframe(X, Y, f, rstride=10, cstride=10)
#     plt.show()


class Fear(GameSystem):
    granulity = NumericProperty(6)

    # static data
    pre_computed_fields = {}

    def init_component(self, cindex, eid, zone, args):
        if 'attraction' not in args:
            args['attraction'] = None
        if 'repulsion' not in args:
            args['repulsion'] = None
        if 'nomove' not in args:
            args['nomove'] = False

        super(Fear, self).init_component(cindex, eid, zone, args)
        comp = self.components[cindex]
        comp.courage = 1.0

    def entity(self, comp):
        if comp is None:
            return None
        return self.gameworld.entities[comp.entity_id]

    def update(self, _dt):
        for c in self.components:
            if c.nomove:
                continue
            vel = Vec2d(0, 0)
            e = self.entity(c)
            x, y = e.position.pos
            for c2 in self.components:
                if c2.entity_id == c.entity_id:
                    continue
                if c2.attraction is None and c2.repulsion is None:
                    continue

                e2 = self.entity(c2)
                x2, y2 = e2.position.pos

                vec = Vec2d(x - x2, y - y2)
                dist2 = vec.get_length_sqrd()

                vecnorm = vec.normalized()

                if c2.repulsion and dist2 < c2.repulsion:
                    vel -= vecnorm

                if c2.attraction and sqrt(dist2) < c2.attraction:
                    vel += vecnorm

            e.cymunk_physics.body.velocity = vel
            e.rotate.r = vel.angle


Factory.register('Fear', cls=Fear)
