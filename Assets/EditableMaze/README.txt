Open Assets/EditableMaze/BallMazeEditable.unity, or menu Ball Maze > Open Editable Scene.

Edit outside Play mode. Expand Walls or Keys in Hierarchy. Move with W; duplicate with Ctrl+D; save with Ctrl+S.
Wall grid spacing: 2 units. Keep key Y around 0.8, player Y around 0.6, exit Y around 0.04.
Prefabs/ contains reusable Wall, Key, Exit and Player. Drag these into the scene.
Keys are counted automatically when Play starts, so duplicated keys need no manual counter change.
Select Player to change acceleration / maxSpeed in MazePlayer.
Keep Player's Game reference and GameManager's Player reference assigned.
Materials/ contains the shared colors; changing a material updates objects that use it.

MazePlayer.cs: input and Rigidbody movement.
MazeKey.cs: rotation and collection trigger.
MazeExit.cs: exit trigger.
MazeGame.cs: timer, key count, win state, restart and HUD.
Editor/EditableMazeBuilder.cs: one-time editor level creation. Runtime does not generate the level.

Original Assets/BallMazeDemo scene is kept separately.
