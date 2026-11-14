package ru.grinko.labnotes;

import android.app.Activity;
import android.os.Bundle;
import android.content.SharedPreferences;
import android.view.MotionEvent;
import android.view.View;
import android.widget.*;
import org.json.JSONArray;
import org.json.JSONException;
import java.util.ArrayList;

public class MainActivity extends Activity {
    private final ArrayList<String> notes = new ArrayList<>();
    private EditText input;
    private LinearLayout list;
    private SharedPreferences storage;
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        storage = getSharedPreferences("notes", MODE_PRIVATE);
        try {
            JSONArray data = new JSONArray(storage.getString("items", "[]"));
            for (int i=0; i<data.length(); i++) notes.add(data.getString(i));
        } catch (JSONException e) { storage.edit().remove("items").apply(); }
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(24, 40, 24, 20);
        TextView title = new TextView(this);
        title.setText("Заметки — ЛР 7"); title.setTextSize(24);
        input = new EditText(this);
        input.setId(101); input.setContentDescription("note-input");
        input.setHint("Текст заметки");
        input.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(200)});
        if (state != null) input.setText(state.getString("draft", ""));
        Button add = new Button(this);
        add.setText("Добавить"); add.setContentDescription("add-note");
        add.setOnClickListener(v -> {
            String text = input.getText().toString().trim();
            if (text.isEmpty()) { input.setError("Введите текст"); return; }
            notes.add(text); input.setText(""); save(); render();
        });
        Button clear = new Button(this);
        clear.setText("Очистить всё"); clear.setContentDescription("clear-notes");
        clear.setOnClickListener(v -> { notes.clear(); save(); render(); });
        list = new LinearLayout(this); list.setOrientation(LinearLayout.VERTICAL);
        ScrollView scroll = new ScrollView(this); scroll.addView(list);
        root.addView(title); root.addView(input); root.addView(add); root.addView(clear);
        root.addView(scroll, new LinearLayout.LayoutParams(-1, 0, 1));
        setContentView(root); render();
    }
    private void save() {
        storage.edit().putString("items", new JSONArray(notes).toString()).apply();
    }
    private void render() {
        list.removeAllViews();
        for (int i=0; i<notes.size(); i++) {
            final int index=i;
            TextView row = new TextView(this);
            row.setText(notes.get(i)); row.setTextSize(20); row.setPadding(12,24,12,24);
            row.setContentDescription("note-"+i);
            row.setOnTouchListener(new View.OnTouchListener() {
                float downX;
                public boolean onTouch(View view, MotionEvent event) {
                    if (event.getAction()==MotionEvent.ACTION_DOWN) { downX=event.getX(); return true; }
                    if (event.getAction()==MotionEvent.ACTION_UP) {
                        if (downX-event.getX()>100) { notes.remove(index); save(); render(); }
                        else view.performClick();
                        return true;
                    }
                    return true;
                }
            });
            list.addView(row);
        }
    }
    @Override public void onSaveInstanceState(Bundle state) {
        state.putString("draft", input.getText().toString());
        super.onSaveInstanceState(state);
    }
}
